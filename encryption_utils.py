"""
Encryption utilities for securing sensitive user data
Uses Fernet (symmetric encryption) from cryptography library
"""
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from typing import Optional

# Load environment variables
load_dotenv()


class FieldEncryption:
    """Handles encryption and decryption of sensitive database fields"""

    def __init__(self):
        # Get encryption key from environment variable
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY not found in environment variables")

        # Initialize Fernet cipher
        self.cipher = Fernet(key.encode())

    def encrypt(self, data: Optional[str]) -> Optional[str]:
        """
        Encrypt a string value

        Args:
            data: Plain text string to encrypt

        Returns:
            Encrypted string (base64 encoded) or None if input is None
        """
        if data is None:
            return None

        if not isinstance(data, str):
            data = str(data)

        # Encrypt and return as string
        encrypted_bytes = self.cipher.encrypt(data.encode())
        return encrypted_bytes.decode()

    def decrypt(self, encrypted_data: Optional[str]) -> Optional[str]:
        """
        Decrypt an encrypted string

        Args:
            encrypted_data: Encrypted string (base64 encoded)

        Returns:
            Decrypted plain text string or None if input is None
        """
        if encrypted_data is None:
            return None

        try:
            # Decrypt and return as string
            decrypted_bytes = self.cipher.decrypt(encrypted_data.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            # If decryption fails, might be unencrypted data (during migration)
            # Return the original value
            print(f"Decryption warning: {str(e)}")
            return encrypted_data


# Global instance to be used across the application
field_encryptor = FieldEncryption()


def encrypt_field(value: Optional[str]) -> Optional[str]:
    """Convenience function to encrypt a field value"""
    return field_encryptor.encrypt(value)


def decrypt_field(value: Optional[str]) -> Optional[str]:
    """Convenience function to decrypt a field value"""
    return field_encryptor.decrypt(value)
