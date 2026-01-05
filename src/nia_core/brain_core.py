"""
Nia LeSane Brain - Core Cognitive Engine
Production-grade error logging for AI reasoning, memory, and decision-making.
"""

import traceback
from datetime import datetime
from typing import Optional, Dict, Any

from logging_config import logger, LogContext


class NiaBrainCore:
    """
    Core cognitive engine for Nia LeSane with comprehensive error logging.
    Handles AI reasoning, memory integration, and decision-making.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Nia Brain Core.
        
        Args:
            config (dict): Configuration dictionary
        """
        try:
            self.config = config or {}
            self.memory_context = {}
            self.conversation_history = []
            logger.info("Nia Brain Core initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Nia Brain Core: {e}", exc_info=True)
            raise
    
    def think(self, prompt: str, context: Optional[Dict] = None) -> Optional[str]:
        """
        Main reasoning function with comprehensive error logging.
        
        Args:
            prompt (str): Input prompt for reasoning
            context (dict): Optional context dictionary
            
        Returns:
            str: Reasoning output or None if failed
        """
        with LogContext("Brain.think()", logger):
            try:
                if not prompt or not isinstance(prompt, str):
                    raise ValueError("Prompt must be a non-empty string")
                
                logger.info(f"Processing prompt: {prompt[:100]}...")
                
                # Integration with memory context
                if context:
                    self.memory_context.update(context)
                    logger.debug(f"Memory context updated with {len(context)} items")
                
                # Simulate reasoning (placeholder for actual LLM integration)
                reasoning_result = self._process_reasoning(prompt)
                
                # Log conversation for audit trail
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "prompt": prompt,
                    "response": reasoning_result
                })
                
                logger.info(f"Reasoning completed successfully, response length: {len(reasoning_result)}")
                return reasoning_result
                
            except ValueError as e:
                logger.warning(f"Invalid input for reasoning: {e}")
                return None
            except Exception as e:
                logger.error(f"Error during reasoning: {e}", exc_info=True)
                raise
    
    def _process_reasoning(self, prompt: str) -> str:
        """
        Internal reasoning processor with error handling.
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            str: Processing result
        """
        with LogContext(f"Brain._process_reasoning()", logger):
            try:
                # Placeholder for actual LLM reasoning logic
                if "error" in prompt.lower():
                    raise RuntimeError("Simulated reasoning error")
                
                result = f"Reasoning response to: {prompt}"
                logger.debug(f"Processed reasoning: {result[:50]}...")
                return result
                
            except Exception as e:
                logger.error(f"Reasoning processing failed: {e}", exc_info=True)
                raise
    
    def recall_memory(self, key: str) -> Optional[Any]:
        """
        Retrieve information from memory with error logging.
        
        Args:
            key (str): Memory key
            
        Returns:
            Any: Stored value or None if not found
        """
        with LogContext(f"Brain.recall_memory({key})", logger):
            try:
                if key in self.memory_context:
                    value = self.memory_context[key]
                    logger.info(f"Memory recalled: {key}")
                    return value
                else:
                    logger.warning(f"Memory key not found: {key}")
                    return None
            except Exception as e:
                logger.error(f"Error recalling memory: {e}", exc_info=True)
                return None
    
    def store_memory(self, key: str, value: Any) -> bool:
        """
        Store information in memory with error logging.
        
        Args:
            key (str): Memory key
            value (Any): Value to store
            
        Returns:
            bool: Success status
        """
        with LogContext(f"Brain.store_memory({key})", logger):
            try:
                if not key:
                    raise ValueError("Memory key cannot be empty")
                
                self.memory_context[key] = value
                logger.info(f"Memory stored: {key} = {type(value).__name__}")
                return True
                
            except Exception as e:
                logger.error(f"Error storing memory: {e}", exc_info=True)
                return False
    
    def get_conversation_history(self) -> list:
        """
        Retrieve conversation history for audit and debugging.
        
        Returns:
            list: Conversation history
        """
        try:
            logger.info(f"Returning conversation history ({len(self.conversation_history)} entries)")
            return self.conversation_history
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {e}", exc_info=True)
            return []


def main():
    """Example usage with error handling."""
    try:
        logger.info("=== Nia Brain Core Demo ===")
        
        brain = NiaBrainCore({"mode": "production"})
        
        # Test thinking
        response = brain.think("What is machine learning?")
        logger.info(f"Brain response: {response}")
        
        # Test memory operations
        brain.store_memory("project_name", "Nia LeSane")
        recalled = brain.recall_memory("project_name")
        logger.info(f"Recalled memory: {recalled}")
        
        logger.info("=== Demo Completed Successfully ===")
        
    except Exception as e:
        logger.critical(f"Critical error in main execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
