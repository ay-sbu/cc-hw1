import abc

import society
from election import Election
from ministry import Ministry
from society import CountryOfficials, Commons

officials = {
    "0": CountryOfficials("0", "1.1.1.1", "85.1.1.1"),

    "1": CountryOfficials("1", "10.1.1.1", "85.1.1.2"),
}
people = {
    "1": Commons("1", "1.1.1.2"),
    "2": Commons("2", "1.1.1.3"),
    "3": Commons("3", "1.1.1.4"),

    "100": Commons("100", "100.1.1.2"),
    "200": Commons("200", "100.1.1.3"),
    "300": Commons("300", "100.1.1.4"),

    "10": Commons("10", "10.1.1.2"),
    "20": Commons("20", "10.1.1.3"),
    "30": Commons("30", "10.1.1.4"),
}
ministry = Ministry("iran", "85.X.X.X")
elections = {}


class State(metaclass=abc.ABCMeta):
    def do_and_get_next(self):
        raise NotImplementedError


class MainState(State):
    def do_and_get_next(self):
        cmd = input("""
        1) enter as official 
        2) vote
        3) exit
        """)
        if cmd == "1":
            nid = input("Enter your national id: ")
            official = officials.get(nid)
            if not official:
                print("You are not found.")
            return OfficialState(official)
        elif cmd == "2":
            return VoteState()
        elif cmd == "3":
            return None
        else:
            return MainState()


class OfficialState(State):
    def __init__(self, official):
        self.official = official

    def do_and_get_next(self):

        cmd = input("""
        0) ..
        1) count votes
        2) finish election
        3) init election
        4) announce election result
        """)

        if cmd == "0":
            return MainState()
        elif cmd == "1":
            return CountingVoteState(self.official)
        elif cmd == "2":
            return FinishVoteState(self.official)
        elif cmd == "3":
            city_id = input("Enter city id: ")
            election = elections.get(city_id)
            if election:
                print("Election already inited.")
                return OfficialState(self.official)
            ip_pattern = input("Enter ip pattern: ")
            election = Election(ministry.country_chain, ministry.public_key, society.Area(city_id, ip_pattern))
            elections[city_id] = election
            return OfficialState(self.official)
        elif cmd == "4":
            city_id = input("Enter city id: ")
            try:
                result, voter_count = ministry.announce_election_result(city_id, self.official.public_ip)
            except Exception as e:
                print(str(e))
                return OfficialState(self.official)
            if result > 0:
                winner = "A won."
            elif result < 0:
                winner = "B won."
            else:
                winner = "Tie"
            print(f"Election result of {city_id} is: {winner} with {abs(result)} more votes in {voter_count} voters.")
            return MainState()
        else:
            return OfficialState(self.official)


class VoteState(State):
    def do_and_get_next(self):
        sure = input("Are you sure? [y/n] ")
        if sure.lower() != "y":
            return MainState()
        city_id = input("Enter city id: ")
        election = elections.get(city_id)
        if election is None:
            print("The election has not started.")
            return MainState()

        nid, raw_vote = input("enter national_id: "), input("enter your vote (A/B): ")
        if raw_vote == "A":
            vote = society.Party.A
        elif raw_vote == "B":
            vote = society.Party.B
        else:
            print("Invalid vote. enter between A or B.")
            return VoteState()
        try:
            person = people.get(nid)
            if not person:
                raise Exception("You are not found")
            election.vote(person, vote)
        except Exception as e:
            print(str(e))
            return MainState()
        print("You voted successfully. Wait for counting results.")
        return MainState()


class CountingVoteState(State):
    def __init__(self, requested_user):
        self.requested_user = requested_user

    def do_and_get_next(self):
        city_id = input("Enter city id: ")
        election = elections.get(city_id)
        if election is None:
            print("The election has not started.")
            return MainState()

        try:
            election.count_votes(self.requested_user)
        except Exception as e:
            print(str(e))
            return OfficialState(self.requested_user)
        print("Votes counted successfully. You can announce it to people.")
        return OfficialState(self.requested_user)


class FinishVoteState(State):
    def __init__(self, requested_user):
        self.requested_user = requested_user

    def do_and_get_next(self):
        city_id = input("Enter city id: ")
        election = elections.get(city_id)
        if election is None:
            print("The election has not started.")
            return MainState()

        try:
            election.finish_election(self.requested_user)
        except Exception as e:
            print(str(e))

        print("Election over.")
        return OfficialState(self.requested_user)


def simulate_without_cheating():
    official = officials.get("0")
    election = Election(ministry.country_chain, ministry.public_key, society.Area("tehran", "1.1.1.X"))

    test_cases = (
        ("1", society.Party.A),
        ("100", society.Party.A),  # out of area
        ("2", society.Party.B),
        ("2", society.Party.B),  # duplicated vote
        ("3", society.Party.B),
    )

    for person_id, vote in test_cases:
        try:
            election.vote(people.get(person_id), vote)
        except Exception as e:
            print(str(e))
            continue
        print("Voted.")
    try:
        election.count_votes(official)
    except Exception as e:
        print(str(e))  # count before finishing election

    election.finish_election(official)
    election.count_votes(official)
    result, voter_count = ministry.announce_election_result("tehran", official.public_ip)
    print(result, voter_count)


def simulate_with_cheating():
    official = officials.get("1")
    election = Election(ministry.country_chain, ministry.public_key, society.Area("tehran", "10.1.1.X"))

    test_cases = (
        ("10", society.Party.A),
        ("20", society.Party.A),
        ("30", society.Party.A),
    )

    for person_id, vote in test_cases:
        election.vote(people.get(person_id), vote)
        print("Voted.")

    election.finish_election(official)
    backup_data = election.local_chain.head.next_block.data
    election.local_chain.head.next_block.data = "poisoned data"  # cheating
    try:
        election.count_votes(official)
    except Exception as e:
        print(str(e))
    election.local_chain.head.next_block.data = backup_data
    election.count_votes(official)
    result, voter_count = ministry.announce_election_result("tehran", official.public_ip)
    print(result, voter_count)


def main():
    state = MainState()
    while state:
        state = state.do_and_get_next()


if __name__ == '__main__':
    # main()
    simulate_with_cheating()
