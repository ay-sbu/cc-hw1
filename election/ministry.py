import phe.paillier

from blockchain import BlockChain
from society import Area


class Ministry:
    def __init__(self, country_name: str, ip_range: str):
        self.country_chain = BlockChain("#")
        self.public_key, self.private_key = phe.paillier.generate_paillier_keypair()
        self.country_chain.add_block(
            f"public_key#{self.public_key.n}"
        )
        self.country = Area(country_name, ip_range)

    def announce_election_result(self, city_id, ip):
        if not self.country.is_ip_in_area_range(ip):
            raise Exception("You should disconnect your vpn.")
        if not self.country_chain.assert_correct():
            raise Exception("Cheating in election result.")

        election_result = self.country_chain.find_block(
            lambda block_data: block_data.startswith(f"result#{city_id}#")
        )
        if not election_result:
            raise Exception("Election votes have not been counted.")

        _, _, voter_count, encrypted_vote_result = election_result.data.split("#")
        return self.private_key.decrypt(phe.paillier.EncryptedNumber(
            self.public_key, int(encrypted_vote_result))), int(voter_count)
