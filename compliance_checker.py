import openai
from dotenv import load_dotenv
import os
from utils import load_url, extract_compliance, ComplianceAnalysis
from pydantic import BaseModel
from typing import List
from functools import lru_cache
from loguru import logger

class ComplianceChecker:
    def __init__(self):
        load_dotenv('.env')
        self.openai_client = openai.OpenAI()

    @lru_cache(maxsize=128)
    def generate_compliance_list(self, url):
        """
        This function takes in a URL and returns a list of compliance rules
        """
        logger.info(f"Generating compliance list from {url}")
        doc_txt = load_url(url)
        compliance_list = extract_compliance(doc_txt)
        return compliance_list
    
    def base_compliance_checker(self, checklist_url: str, target_url: str):
        """
        This function takes in a compliance checklist and a target document, and returns a list of compliance checks
        """
        compliance_list = self.generate_compliance_list(checklist_url)
        logger.info(f"Checking compliance for {target_url}")
        system_msg = f"""
        You are a compliance expert, here is the compliance checklist,  
        {compliance_list}
        Based on this checklist, please check and provide which compliance rules are met in the document
        """
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": load_url(target_url)}
        ]
        response = self.openai_client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            response_format= ComplianceAnalysis
        )
        response = response.to_dict()
        compliance_checks = response['choices'][0]['message']['parsed']['compliance_checks']
         # genarate compliance score 
        compliance_score = 0
        for check in compliance_checks:
            if check['compliant']:
                compliance_score += 1
        compliance_score = (compliance_score / len(compliance_checks)) * 100
        compliance_analysis = {
            "compliance_checks": compliance_checks,
            "compliance_score": compliance_score
        }
        return compliance_analysis

    def chain_compliance_checker(self, checklist_url: str, target_url: str):
        """
        This function takes in a compliance checklist and a target document, and returns a list of compliance checks
        It uses a chain of thought approach to first generate an analysis of the document based on the checklist
        then uses the analysis to generate a more detailed compliance check
        """
        compliance_list = self.generate_compliance_list(checklist_url)
        logger.info(f"Checking compliance for {target_url}")
        init_system_msg = f"""
        You are a compliance expert, here is the compliance checklist,
        {compliance_list}
        Based on this checklist, generate an extensive report on the compliance status of the document
        """
        messages = [
            {"role": "system", "content": init_system_msg},
            {"role": "user", "content": load_url(target_url)}
        ]
        init_response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.0
        )
        init_response = init_response.to_dict()
        init_response = init_response['choices'][0]['message']['content']
        logger.info("Intial Analsysis: ", init_response)
        sys_msg = f"""
        You are a compliance expert, here is the compliance checklist,
        {compliance_list}
        Here is an initial report on the compliance status of the document
        {init_response}
        Based on the checklist, and the document, please provide a compliance analysis
        """
        messages = [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": load_url(target_url)}
        ]
        response = self.openai_client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            response_format= ComplianceAnalysis
        )
        response = response.to_dict()
        compliance_checks = response['choices'][0]['message']['parsed']['compliance_checks']
        # genarate compliance score 
        compliance_score = 0
        for check in compliance_checks:
            if check['compliant']:
                compliance_score += 1
        compliance_score = (compliance_score / len(compliance_checks)) * 100
        compliance_analysis = {
            "compliance_checks": compliance_checks,
            "compliance_score": compliance_score
        }
        return compliance_analysis
