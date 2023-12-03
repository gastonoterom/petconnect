import bcrypt

from infrastructure.background import run_async


class CryptoUtils:
    @staticmethod
    async def hash_string(string_to_hash: str) -> str:
        def _hash_string_sync() -> str:
            # Blocking I/O method
            salt = bcrypt.gensalt()
            hash_bytes: bytes = string_to_hash.encode("utf8")
            hash_str = bcrypt.hashpw(hash_bytes, salt).decode("utf8")
            return hash_str

        return await run_async(_hash_string_sync)

    @staticmethod
    async def verify_hash(string_to_verify: str, hash_to_verify: str) -> bool:
        def _verify_hash_sync() -> bool:
            # Blocking I/O method

            check_hash = bcrypt.checkpw(
                string_to_verify.encode("utf8"),
                hash_to_verify.encode("utf8"),
            )

            return check_hash

        return await run_async(_verify_hash_sync)
