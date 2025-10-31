"""
Unit tests for LLM Manager
Tests the centralized LLM manager and API wrapper
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)


@pytest.mark.unit
class TestLLMManager:
    """Tests for LLM Manager"""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_no_api_token(self):
        """Test initialization without API token"""
        # Reload module to test without token
        import importlib
        import src.core.llm_manager as llm_module
        
        # Clear any existing llama instance
        if hasattr(llm_module, 'llama'):
            delattr(llm_module, 'llama')
        
        # Mock logger to avoid warnings during test
        with patch('src.core.llm_manager.logger'):
            importlib.reload(llm_module)
            
            # llama should be None when no token
            assert llm_module.llama is None or llm_module.llama is None
    
    @patch.dict(os.environ, {'HUGGINGFACE_API_TOKEN': 'test_token_123'})
    @patch('src.core.llm_manager.InferenceClient')
    def test_with_api_token(self, mock_client_class):
        """Test initialization with API token"""
        import importlib
        import src.core.llm_manager as llm_module
        
        # Setup mock client
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Reload module
        if hasattr(llm_module, 'llama'):
            delattr(llm_module, 'llama')
        
        with patch('src.core.llm_manager.logger'):
            importlib.reload(llm_module)
            
            # llama should be initialized
            assert llm_module.llama is not None
            assert hasattr(llm_module.llama, '__call__')
    
    @patch.dict(os.environ, {'HUGGINGFACE_API_TOKEN': 'test_token_123'})
    @patch('src.core.llm_manager.InferenceClient')
    def test_api_wrapper_call(self, mock_client_class):
        """Test API wrapper call method"""
        import importlib
        import src.core.llm_manager as llm_module
        
        # Setup mock client with chat_completion method
        mock_client = Mock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat_completion.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Reload module
        if hasattr(llm_module, 'llama'):
            delattr(llm_module, 'llama')
        
        with patch('src.core.llm_manager.logger'):
            importlib.reload(llm_module)
            
            # Test calling the wrapper
            if llm_module.llama is not None:
                prompt = "Test prompt"
                result = llm_module.llama(prompt)
                
                assert result is not None
                assert isinstance(result, list)
                assert len(result) > 0
                assert "generated_text" in result[0]
    
    @patch.dict(os.environ, {'HUGGINGFACE_API_TOKEN': 'test_token_123'})
    @patch('src.core.llm_manager.InferenceClient')
    def test_api_wrapper_prompt_parsing(self, mock_client_class):
        """Test API wrapper parses Llama 3 prompt format"""
        import importlib
        import src.core.llm_manager as llm_module
        
        # Setup mock client
        mock_client = Mock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat_completion.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Reload module
        if hasattr(llm_module, 'llama'):
            delattr(llm_module, 'llama')
        
        with patch('src.core.llm_manager.logger'):
            importlib.reload(llm_module)
            
            if llm_module.llama is not None:
                # Test with Llama 3 formatted prompt
                prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
System message<|eot_id|><|start_header_id|>user<|end_header_id|>
User message<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
                result = llm_module.llama(prompt)
                
                # Verify chat_completion was called with parsed messages
                assert mock_client.chat_completion.called
                call_args = mock_client.chat_completion.call_args
                assert 'messages' in call_args.kwargs
                messages = call_args.kwargs['messages']
                assert len(messages) > 0
    
    @patch.dict(os.environ, {'HUGGINGFACE_API_TOKEN': 'test_token_123'})
    @patch('src.core.llm_manager.InferenceClient')
    def test_api_wrapper_error_handling(self, mock_client_class):
        """Test API wrapper error handling"""
        import importlib
        import src.core.llm_manager as llm_module
        
        # Setup mock client that raises exception
        mock_client = Mock()
        mock_client.chat_completion.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client
        
        # Reload module
        if hasattr(llm_module, 'llama'):
            delattr(llm_module, 'llama')
        
        with patch('src.core.llm_manager.logger'):
            importlib.reload(llm_module)
            
            if llm_module.llama is not None:
                prompt = "Test prompt"
                result = llm_module.llama(prompt)
                
                # Should return fallback response on error
                assert result is not None
                assert isinstance(result, list)
                assert "generated_text" in result[0]
                # Should contain error message or fallback text
                assert "ошибка" in result[0]["generated_text"].lower() or "error" in result[0]["generated_text"].lower()


@pytest.mark.unit
class TestLLMManagerIntegration:
    """Integration-style tests for LLM Manager"""
    
    @patch.dict(os.environ, {'HUGGINGFACE_API_TOKEN': 'test_token_123'})
    @patch('src.core.llm_manager.InferenceClient')
    def test_model_name_configuration(self, mock_client_class):
        """Test that correct model name is configured"""
        import importlib
        import src.core.llm_manager as llm_module
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Reload module
        if hasattr(llm_module, 'llama'):
            delattr(llm_module, 'llama')
        
        with patch('src.core.llm_manager.logger'):
            importlib.reload(llm_module)
            
            # Verify model name
            assert hasattr(llm_module, 'MODEL_NAME')
            assert "llama" in llm_module.MODEL_NAME.lower() or "meta" in llm_module.MODEL_NAME.lower()

