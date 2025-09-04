#!/usr/bin/env python3
"""
Backend API Testing Suite for Portfolio Website
Tests all backend endpoints and functionality
"""

import requests
import json
import os
import tempfile
import time
from typing import Dict, Any, Optional
from pathlib import Path

class BackendTester:
    def __init__(self):
        # Get backend URL from frontend .env
        self.base_url = self._get_backend_url()
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.test_results = {}
        
    def _get_backend_url(self) -> str:
        """Get backend URL from frontend .env file"""
        try:
            env_path = Path("/app/frontend/.env")
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('REACT_APP_BACKEND_URL='):
                            return line.split('=', 1)[1].strip()
            return "http://localhost:8001"  # fallback
        except Exception as e:
            print(f"Error reading frontend .env: {e}")
            return "http://localhost:8001"
    
    def log_test(self, test_name: str, success: bool, message: str, details: Optional[Dict] = None):
        """Log test results"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'details': details or {}
        }
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            print(f"   Details: {details}")
    
    def test_health_endpoints(self):
        """Test health check endpoints"""
        print("\n=== Testing Health Endpoints ===")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{self.api_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "version" in data:
                    self.log_test("Root Health Check", True, "Root endpoint working", data)
                else:
                    self.log_test("Root Health Check", False, "Invalid response format", {"response": data})
            else:
                self.log_test("Root Health Check", False, f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test("Root Health Check", False, f"Connection error: {str(e)}")
        
        # Test health endpoint
        try:
            response = self.session.get(f"{self.api_url}/health")
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("Health Check", True, "Health endpoint working", data)
                else:
                    self.log_test("Health Check", False, "Unhealthy status", data)
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
    
    def test_contact_form_basic(self):
        """Test basic contact form submission without file"""
        print("\n=== Testing Contact Form - Basic Submission ===")
        
        form_data = {
            'name': 'John Smith',
            'email': 'john.smith@example.com',
            'subject': 'Portfolio Inquiry - Data Science Position',
            'message': 'Hi Shubham, I came across your portfolio and I am impressed with your data science projects. I would like to discuss a potential opportunity at our company. Could we schedule a call this week?',
            'phone': '+1-555-0123',
            'company': 'Tech Innovations Inc'
        }
        
        try:
            response = self.session.post(f"{self.api_url}/contact", data=form_data)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['id', 'name', 'email', 'subject', 'message', 'submitted_at', 'status']
                
                if all(field in data for field in required_fields):
                    self.log_test("Contact Form Basic", True, "Form submitted successfully", {
                        "id": data.get('id'),
                        "status": data.get('status'),
                        "has_attachment": data.get('has_attachment', False)
                    })
                    return data.get('id')  # Return ID for further tests
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Contact Form Basic", False, f"Missing fields: {missing}", data)
            else:
                self.log_test("Contact Form Basic", False, f"HTTP {response.status_code}", {
                    "response": response.text[:500]
                })
        except Exception as e:
            self.log_test("Contact Form Basic", False, f"Request error: {str(e)}")
        
        return None
    
    def test_contact_form_with_file(self):
        """Test contact form submission with file attachment"""
        print("\n=== Testing Contact Form - With File Upload ===")
        
        # Create a test PDF file
        test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n202\n%%EOF"
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(test_content)
            tmp_file.flush()
            
            form_data = {
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@techcorp.com',
                'subject': 'Resume Submission - Senior Data Analyst Role',
                'message': 'Hello Shubham, I am reaching out regarding the Senior Data Analyst position. Please find my resume attached. I have 5+ years of experience in data analysis and machine learning.',
                'company': 'TechCorp Solutions'
            }
            
            try:
                with open(tmp_file.name, 'rb') as f:
                    files = {'file': ('resume.pdf', f, 'application/pdf')}
                    response = self.session.post(f"{self.api_url}/contact", data=form_data, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('has_attachment') and data.get('attachment_filename'):
                        self.log_test("Contact Form File Upload", True, "File uploaded successfully", {
                            "id": data.get('id'),
                            "attachment_filename": data.get('attachment_filename'),
                            "has_attachment": data.get('has_attachment')
                        })
                        return data.get('id')
                    else:
                        self.log_test("Contact Form File Upload", False, "File not processed", data)
                else:
                    self.log_test("Contact Form File Upload", False, f"HTTP {response.status_code}", {
                        "response": response.text[:500]
                    })
            except Exception as e:
                self.log_test("Contact Form File Upload", False, f"Request error: {str(e)}")
            finally:
                # Clean up temp file
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
        
        return None
    
    def test_file_validation(self):
        """Test file upload validation"""
        print("\n=== Testing File Upload Validation ===")
        
        # Test oversized file (simulate 6MB file)
        large_content = b"x" * (6 * 1024 * 1024)  # 6MB
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(large_content)
            tmp_file.flush()
            
            form_data = {
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'File Size Test',
                'message': 'Testing file size validation'
            }
            
            try:
                with open(tmp_file.name, 'rb') as f:
                    files = {'file': ('large_file.pdf', f, 'application/pdf')}
                    response = self.session.post(f"{self.api_url}/contact", data=form_data, files=files)
                
                if response.status_code == 400:
                    self.log_test("File Size Validation", True, "Large file rejected correctly", {
                        "status_code": response.status_code
                    })
                else:
                    self.log_test("File Size Validation", False, f"Expected 400, got {response.status_code}")
            except Exception as e:
                self.log_test("File Size Validation", False, f"Request error: {str(e)}")
            finally:
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
        
        # Test invalid file type
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp_file:
            tmp_file.write(b"fake executable content")
            tmp_file.flush()
            
            try:
                with open(tmp_file.name, 'rb') as f:
                    files = {'file': ('malware.exe', f, 'application/x-executable')}
                    response = self.session.post(f"{self.api_url}/contact", data=form_data, files=files)
                
                if response.status_code == 400:
                    self.log_test("File Type Validation", True, "Invalid file type rejected", {
                        "status_code": response.status_code
                    })
                else:
                    self.log_test("File Type Validation", False, f"Expected 400, got {response.status_code}")
            except Exception as e:
                self.log_test("File Type Validation", False, f"Request error: {str(e)}")
            finally:
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
    
    def test_form_validation(self):
        """Test form field validation"""
        print("\n=== Testing Form Validation ===")
        
        # Test missing required fields
        invalid_forms = [
            ({}, "Empty form"),
            ({'name': 'John'}, "Missing email, subject, message"),
            ({'name': 'John', 'email': 'invalid-email'}, "Invalid email format"),
            ({'name': 'A', 'email': 'test@example.com', 'subject': 'Hi', 'message': 'Short'}, "Too short fields"),
            ({'name': '', 'email': 'test@example.com', 'subject': 'Test', 'message': 'Test message'}, "Empty name"),
        ]
        
        for form_data, test_desc in invalid_forms:
            try:
                response = self.session.post(f"{self.api_url}/contact", data=form_data)
                
                if response.status_code == 400 or response.status_code == 422:
                    self.log_test(f"Validation - {test_desc}", True, "Invalid form rejected correctly", {
                        "status_code": response.status_code
                    })
                else:
                    self.log_test(f"Validation - {test_desc}", False, f"Expected 400/422, got {response.status_code}")
            except Exception as e:
                self.log_test(f"Validation - {test_desc}", False, f"Request error: {str(e)}")
    
    def test_get_contact_messages(self):
        """Test retrieving contact messages (admin endpoint)"""
        print("\n=== Testing Get Contact Messages ===")
        
        try:
            response = self.session.get(f"{self.api_url}/contact")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get Contact Messages", True, f"Retrieved {len(data)} messages", {
                        "count": len(data),
                        "sample": data[0] if data else None
                    })
                else:
                    self.log_test("Get Contact Messages", False, "Response not a list", {"response": data})
            else:
                self.log_test("Get Contact Messages", False, f"HTTP {response.status_code}", {
                    "response": response.text[:500]
                })
        except Exception as e:
            self.log_test("Get Contact Messages", False, f"Request error: {str(e)}")
    
    def test_message_status_update(self, message_id: str):
        """Test updating message status"""
        if not message_id:
            self.log_test("Message Status Update", False, "No message ID available for testing")
            return
        
        print(f"\n=== Testing Message Status Update (ID: {message_id[:8]}...) ===")
        
        try:
            response = self.session.patch(f"{self.api_url}/contact/{message_id}/status?status=read")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'read':
                    self.log_test("Message Status Update", True, "Status updated successfully", data)
                else:
                    self.log_test("Message Status Update", False, "Status not updated", data)
            else:
                self.log_test("Message Status Update", False, f"HTTP {response.status_code}", {
                    "response": response.text[:500]
                })
        except Exception as e:
            self.log_test("Message Status Update", False, f"Request error: {str(e)}")
    
    def test_database_persistence(self):
        """Test database data persistence"""
        print("\n=== Testing Database Persistence ===")
        
        # Submit a form and then retrieve it
        form_data = {
            'name': 'Database Test User',
            'email': 'dbtest@example.com',
            'subject': 'Database Persistence Test',
            'message': 'This message is for testing database persistence functionality.'
        }
        
        try:
            # Submit form
            submit_response = self.session.post(f"{self.api_url}/contact", data=form_data)
            
            if submit_response.status_code == 200:
                submit_data = submit_response.json()
                message_id = submit_data.get('id')
                
                # Wait a moment for database write
                time.sleep(1)
                
                # Retrieve messages
                get_response = self.session.get(f"{self.api_url}/contact")
                
                if get_response.status_code == 200:
                    messages = get_response.json()
                    
                    # Find our message
                    found_message = None
                    for msg in messages:
                        if msg.get('id') == message_id:
                            found_message = msg
                            break
                    
                    if found_message:
                        # Verify data integrity
                        if (found_message.get('name') == form_data['name'] and
                            found_message.get('email') == form_data['email'] and
                            found_message.get('subject') == form_data['subject']):
                            self.log_test("Database Persistence", True, "Data persisted correctly", {
                                "message_id": message_id,
                                "retrieved_data": {
                                    "name": found_message.get('name'),
                                    "email": found_message.get('email'),
                                    "subject": found_message.get('subject')
                                }
                            })
                        else:
                            self.log_test("Database Persistence", False, "Data corruption detected", {
                                "expected": form_data,
                                "retrieved": found_message
                            })
                    else:
                        self.log_test("Database Persistence", False, "Message not found in database", {
                            "message_id": message_id,
                            "total_messages": len(messages)
                        })
                else:
                    self.log_test("Database Persistence", False, f"Failed to retrieve messages: HTTP {get_response.status_code}")
            else:
                self.log_test("Database Persistence", False, f"Failed to submit form: HTTP {submit_response.status_code}")
        except Exception as e:
            self.log_test("Database Persistence", False, f"Request error: {str(e)}")
    
    def test_email_service_configuration(self):
        """Test email service configuration (non-functional test)"""
        print("\n=== Testing Email Service Configuration ===")
        
        # This tests if email service is configured, not if emails are actually sent
        # since we don't have real SMTP credentials
        
        form_data = {
            'name': 'Email Test User',
            'email': 'emailtest@example.com',
            'subject': 'Email Service Test',
            'message': 'Testing email service integration and configuration.'
        }
        
        try:
            response = self.session.post(f"{self.api_url}/contact", data=form_data)
            
            if response.status_code == 200:
                # Email service errors should not prevent form submission
                # They should be logged but not cause API failure
                self.log_test("Email Service Integration", True, "Email service integrated (may show warnings in logs)", {
                    "note": "SMTP configuration required for actual email sending"
                })
            else:
                self.log_test("Email Service Integration", False, f"Form submission failed: HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Email Service Integration", False, f"Request error: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting Backend API Tests")
        print(f"Backend URL: {self.base_url}")
        print(f"API URL: {self.api_url}")
        print("=" * 60)
        
        # Run tests in order
        self.test_health_endpoints()
        self.test_form_validation()
        self.test_file_validation()
        
        # Test basic form submission and get ID for further tests
        message_id = self.test_contact_form_basic()
        
        # Test file upload
        file_message_id = self.test_contact_form_with_file()
        
        # Test database operations
        self.test_database_persistence()
        self.test_get_contact_messages()
        
        # Test status update if we have a message ID
        if message_id:
            self.test_message_status_update(message_id)
        
        # Test email service integration
        self.test_email_service_configuration()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("🔍 BACKEND TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results.values() if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        print("\n📋 Detailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status} {test_name}: {result['message']}")
        
        # Critical issues
        critical_failures = []
        for test_name, result in self.test_results.items():
            if not result['success'] and any(keyword in test_name.lower() for keyword in ['health', 'basic', 'database']):
                critical_failures.append(test_name)
        
        if critical_failures:
            print(f"\n🚨 CRITICAL FAILURES:")
            for failure in critical_failures:
                print(f"   - {failure}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()