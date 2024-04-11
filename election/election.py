import datetime

import phe

import society
from blockchain import BlockChain


class Election:

    def __init__(
            self,
            country_blockchain: BlockChain,
            ministry_public_key: phe.PaillierPublicKey,
            city: society.Area,
    ):
        self.country_chain = country_blockchain
        self.local_chain = BlockChain("#")
        self.local_chain.add_block(
            f"public_key#{ministry_public_key.n}"
        )
        self.city = city

    @property
    def public_key(self) -> phe.PaillierPublicKey:
        public_key_block = self.local_chain.find_block(lambda block_data: block_data.startswith("public_key#"))
        if not public_key_block:
            raise Exception("Public key not found")
        _, raw_public_key = public_key_block.data.split("#")
        return phe.PaillierPublicKey(int(raw_public_key))

    def already_voted(self, person: society.Commons):
        vote = self.local_chain.find_block(
            lambda block_data: block_data.startswith(f"vote#{person.hashed_national_code}")
        )
        return vote is not None

    def election_is_over(self):
        election_finish_flag = self.local_chain.find_block(
            lambda block_data: block_data.startswith("finish#")
        )
        return election_finish_flag is not None

    def vote(self, person: society.Commons, party: society.Party):
        if not self.city.is_ip_in_area_range(person.ip):
            raise Exception("You can vote only in city area.")
        if self.election_is_over():
            raise Exception("Election is over")
        if self.already_voted(person):
            raise Exception("Duplicated vote")

        self.local_chain.add_block(
            f"vote#{person.hashed_national_code}#{self.public_key.encrypt(party.value).ciphertext()}"
        )

    def finish_election(self, requested_person):
        if not self.city.is_ip_in_area_range(requested_person.ip):
            raise Exception("You can finish election only in city area.")
        if self.election_is_over():
            raise Exception("Election is already over.")

        self.local_chain.add_block(f"finish#{datetime.datetime.now().timestamp()}")

    def count_votes(self, requested_person):
        if not self.city.is_ip_in_area_range(requested_person.ip):
            raise Exception("You can count votes only in city area.")
        if not self.election_is_over():
            raise Exception("Election isn't over.")
        if not self.local_chain.assert_correct():
            raise Exception("The election was rigged.")

        current_block = self.local_chain.head
        sum_votes = self.public_key.encrypt(0)
        voter_count = 0
        while current_block:
            data_type, payload = current_block.data.split("#", 1)
            if data_type != "vote":
                current_block = current_block.next_block
                continue
            _, raw_vote = payload.split("#")
            vote = phe.paillier.EncryptedNumber(self.public_key, int(raw_vote))
            sum_votes += vote
            voter_count += 1

            current_block = current_block.next_block

        self.local_chain.add_block(
            f"result#{voter_count}#{sum_votes.ciphertext()}"
        )
        self.country_chain.add_block(
            f"result#{self.city.id}#{voter_count}#{sum_votes.ciphertext()}"
        )
