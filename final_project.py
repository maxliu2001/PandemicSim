import random
from typing import List
from uuid import uuid4


class CountryA:
    def __init__(self, name: str):
        self.name = name

    def msort_large(self, list: List["Person"]): #merge sort for Country A citizens
        if len(list) < 2:
            return list
        result = []  # moved!
        mid = int(len(list) / 2)
        y = self.msort_large(list[:mid])
        z = self.msort_large(list[mid:])
        while (len(y) > 0) and (len(z) > 0): #breaking down the list
            if y[0].rel_scale > z[0].rel_scale: #sort list based on relevance scale
                result.append(z[0])
                z.pop(0)
            else:
                result.append(y[0])
                y.pop(0)
        result += y
        result += z
        return result

    def distribute_disease_at_very_first(self, country: "CountryB"):
        citizens = country.get_citizens()
        sorted_rel_3 = self.msort_large(citizens)
        distribute_num_3 = int(len(sorted_rel_3) * 0.1) #determine the number of people to infect
        for person in sorted_rel_3[len(sorted_rel_3) - distribute_num_3:]:
            person.infection = 3 #spread disease


class CountryB:
    def __init__(self, name: str):
        self.name = name
        self.citizens = []  # store all living citizens
        self.infected_rate = 0
        self.towns = [] #store all towns
        self.distributeA = False

    def rate_of_v(self):
        v = 0
        rate_of_vaccine = None
        for person in self.citizens:

            if person.vaccine == True:
                v += 1
        rate_of_vaccine = float(v / len(self.citizens)) #calculate number of people who take vaccine divided by population
        return rate_of_vaccine

    def rate_of_a(self):
        a = 0
        rate_of_antidote = None
        for person in self.citizens:

            if person.antidote == True:
                a += 1
        rate_of_antidote = float(a / len(self.citizens)) #calculate number of people who take antidotes divided by population
        return rate_of_antidote

    "get everything"

    def get_citizens(self):
        all_towns = self.get_towns()
        for town in all_towns:
            citizens = town.get_resident()
            for each in citizens:
                self.citizens.append(each) #append each resident of town into citizen list
        return self.citizens

    def get_towns(self):
        return self.towns

    "town movement"

    def add_town(self, town: "Town"):
        self.towns.append(town)

    def remove_town(self, town: "Town"):
        if town in self.towns:
            self.towns.remove(town)
        else:
            print("Invalid entry")

    # infection_rate = dead_person + infected_person
    "infection rate of countryB"

    # def set_infection_rate(self):
    # count_sick = 0
    # count_dead = 0
    # for town in self.towns:
    # count_dead += len(town.tombs)
    # for person in self.citizens:
    # if person.infection >= 3:
    # count_sick += 1
    # self.infected_rate = float(count_sick / (len(self.citizens) + count_dead))
    # return self.infected_rate

    def set_infection_rate(self):
        count_sick = 0
        count_dead = 0
        for person in self.citizens:
            if person.dead == True: #count dead people
                count_dead += 1
            if person.dead == True or person.infection >= 3: #count sick people
                count_sick += 1
        self.infected_rate = float(count_sick / (len(self.citizens) + count_dead)) #set infected rate
        return self.infected_rate

    "distribute antibody"

    def distribute_antibody(self):
        x = int(0.2 * len(self.citizens))
        i = 0
        person_with_antibody = set()
        for i in range(x):
            select = random.choice(self.citizens)  #randomly distribute antibodies
            person_with_antibody.add(select)
            for person in person_with_antibody:
                person.antibody = True
            i += 1

    "distribute antidote"

    def _msort(self, list: List["Person"]): #merge sort for antidote distribution based on rel_scale
        if len(list) < 2:
            return list
        result = []  # moved!
        mid = int(len(list) / 2)
        y = self._msort(list[:mid])
        z = self._msort(list[mid:])
        while (len(y) > 0) and (len(z) > 0):
            if y[0].rel_scale > z[0].rel_scale:
                result.append(z[0])
                z.pop(0)
            else:
                result.append(y[0])
                y.pop(0)
        result += y
        result += z
        return result

    def check_if_distribute_a(self):
        all_res = self.citizens
        for person in all_res:
            if person.antibody == True and person.infection >= 3: #check if distribution meets requirement
                self.distributeA = True
                self.distribute_antidote()
            # trigger research

    def distribute_antidote(self): #distribute antidote based on rel_scale
        if self.distributeA:
            rel_scale_l_2 = []
            citizens = self.citizens
            for person in citizens:
                if person.antidote == False:
                    rel_scale_l_2.append(person)
            sorted_rel_2 = self._msort(rel_scale_l_2)
            distribute_num_2 = int(len(sorted_rel_2) * 0.15)
            for person in sorted_rel_2[len(sorted_rel_2) - distribute_num_2:]:
                person.antidote = True

    def function_antidote(self):  #antidote functions for people
        citizens = self.citizens
        for person in citizens:
            if person.antidote == True:
                person.infection -= 0.1


class Town:
    def __init__(self, name: str):
        self.uid = uuid4()
        self.name = name
        self.residents = []
        self.quarantine = None
        self.infection_rate = 0
        self.distributeV = False
        self.tombs = []

    def __contains__(self, person: "Person"):  # check if certain person is hosted in town
        return person in self.residents

    def get_resident(self):  # get method for people in town
        return self.residents  # return the set of residents

    def add_resident(self, person: "Person"):  # add new resident to the exsisting residents list
        self.residents.append(person)
        return self.residents

    def remove_resident(self, person: "Person"):  # moves a residents from the list of residents from town
        if person in self.residents:
            self.residents.remove(person)
        else:
            print("Entry invalid")
        # return self

    def set_infection_rate(self): #calculate infection rate for town
        count_sick = float(0)
        count_dead = 0. + float(len(self.tombs))
        for person in self.residents:
            if person.infection >= 3:
                count_sick += float(1)
        self.infection_rate = float(count_sick / (float(len(self.residents)) + count_dead))
        return self.infection_rate

    def check_if_quarantine(self):
        if self.infection_rate >= 0.8: #check if town meets quarantine standard
            self.start_quarantine()

    def start_quarantine(self): #start quaratine by deleting all residents
        for person in self.residents:
            person.set_dead()

    def check_if_distribute_v(self): #check if town meets vaccine distribution requirement
        count_sick = 0. + len(self.tombs)
        for person in self.residents:
            if person.infection >= 3:
                count_sick += 1
        if float(count_sick / len(self.residents)) >= 0.15:
            self.distributeV = True
            self.distribute_vaccine()

    def msort(self, list: List["Person"]): #merge sort based on rel_scale for vaccine
        if len(list) < 2:
            return list
        result = []  # moved!
        mid = int(len(list) / 2)
        y = self.msort(list[:mid])
        z = self.msort(list[mid:])
        while (len(y) > 0) and (len(z) > 0):
            if y[0].rel_scale > z[0].rel_scale:
                result.append(z[0])
                z.pop(0)
            else:
                result.append(y[0])
                y.pop(0)
        result += y
        result += z
        return result

    def distribute_vaccine(self): #distribute vaccine based on rel_scale
        if self.distributeV:
            rel_scale_l = []
            for person in self.residents:
                if person.infection <= 3 and person.vaccine == False:
                    rel_scale_l.append(person)
            sorted_rel = self.msort(rel_scale_l)
            # print(sorted_rel)
            distribute_num = int(len(sorted_rel) * 0.9)
            for person in sorted_rel[len(sorted_rel) - distribute_num:]:
                person.vaccine = True


class Person:

    def __init__(self, name: str):
        self.uid = uuid4()
        self.name = name
        self.friends = []
        self.family = []
        self.infection = 0
        self.vaccine = False
        self.dead = False
        self.rel_scale = 0
        self.antibody = False
        self.dead = False
        self.infected = False
        self.antidote = False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Person<{self.name}, {self.uid}>"

    def get_country(self):
        if self in CountryB.get_citizens():
            return CountryB

    def get_name(self):  # get name of person object
        return self.name

    def get_id(self):
        return self.uid

    def get_friends(self):
        return self.friends

    def add_friend(self, person: "Person"):
        self.friends.append(person)  # add person to list of friends
        person.friends.append(self)
        person.rel_scale += 0.5
        self.rel_scale += 1  # every time this person is friended by someone else the rel_scale increases by 1

    def add_family(self, person: "Person"):
        self.family.append(person)  # add family to list of families
        person.family.append(self)
        person.rel_scale += 1.5
        self.rel_scale += 3

    def check_if_dead(self, country: CountryB): #check if a person is dead and delete that individual
        if self.infection == 5:
            self.dead = True
            self.set_dead(country)
            # return self

    def set_dead(self, country: CountryB):
        town = self.get_town_of_person(country)
        town.remove_resident(self)
        town.tombs.append(self)

    def check_if_infected(self): #check if a person meets requirement for infecting others
        if self.infection >= 3:
            self.infected = True

    # return the town a person is staying
    def get_town_of_person(self, country: CountryB):
        # find the town of person
        all_towns = country.towns
        for town in all_towns:
            P = town.get_resident()
            IDD = self.uid
            for n in P:
                if n.uid == IDD:
                    return town

    "infected functions"

    def infect_neighbours(self, country: CountryB): #infect people who live in the same town with a person
        # town = self.get_town_of_person(country)
        # print(town)
        for town in country.towns:
            if self in town.residents:
                for person in town.residents:
                    if person.vaccine == True:
                        person.infection += 0.005
                    else:
                        person.infection += 0.05

    def infect_friends(self): #infect friends of a person
        friends = self.friends
        for person in friends:
            if person.vaccine == True:
                person.infection += 0.01
            else:
                person.infection += 0.1

    def infect_family(self): #infect families of a person
        family = self.family
        for person in family:
            if person.vaccine == True:
                person.infection += 0.01
            else:
                person.infection += 0.15


class Day:
    def __init__(self, day=0):
        self.day = day

    def a_day_pass(self, country: CountryB): #defines what happens during a day
        ##infect the family
        for person in country.citizens:
            person.check_if_dead(country)
            if person.infection >= 3: #check if a person is contagious
                # infection + vaccine

                person.infect_family()
                person.infect_friends()
                person.infect_neighbours(country)
                # antidote

        for town in country.towns:
            town.set_infection_rate()  # get town infection rate
            town.check_if_quarantine()
            town.check_if_distribute_v()

        country.set_infection_rate()#get country infection rate
        country.check_if_distribute_a() #check antidote distribution
        country.function_antidote()

        if country.distributeA == True: #antidote distribution in country B
            country.distribute_antidote()

        for town in country.towns: #vaccine distribution in a town
            if town.distributeV == True:
                town.distribute_vaccine()
        self.day += 1

    def research_antidote(self, country: CountryB):
        population = len(country.citizens)
        research_days = int(500 / population) #determines the days country B takes to research antidote
        i = 0
        for i in range(research_days):
            self.a_day_pass(country)
            i += 1

        if self.day == research_days:
            country.distributeA = True
            country.distribute_antibody()
    # return person.infection


class Global:
    def __init__(self, country: "CountryB", day: int, day_class: Day):
        self.country = country
        self.day = day

        for i in range(int(self.day)):
            i = 0
            day_class.a_day_pass(country)
            i += 1

    def get_infected_rate_country(self, country: "CountryB"): #get country infection rate
        return country.set_infection_rate()

    def get_infected_rate_town(self): #get infection rate for each town and return as a list
        town_rate_list = []
        for town in self.country.towns:
            town_rate_list.append(town.set_infection_rate())
        return town_rate_list

    def get_population(self): #get living population of country B
        # total = 0
        # for town in self.country.towns:
        # total += int(len(town.tombs))
        # return int(len(self.country.citizens)) - total
        total = 0
        for towns in self.country.towns:
            total += len(towns.residents)
        for citizen in self.country.citizens:
            dead = 0
            if citizen.infection == 5:
                dead += 1
        return total - dead

    def get_vaccine_rate(self, country: "CountryB"): #get vaccine rate for country B
        return country.rate_of_v()

    def get_antidote_rate(self, country: "CountryB"): #get antidote rate for country B
        return country.rate_of_a()

    def get_research_days(self): #get research day to research antidote
        return int(500 / self.get_population())


def main(k): #test case used for presentation
    michael = Person("Michael")
    jack = Person("Jack")
    kyle = Person("Kyle")
    charlie = Person("Charlie")
    bob = Person("Bob")
    annie = Person("Annie")
    max = Person("Max")
    alex = Person("Alex")
    mats = Person("Mats")
    sami = Person("Sami")
    ryan = Person("Ryan")
    josh = Person("Josh")
    nate = Person("Nate")
    kate = Person("Kate")
    james = Person("James")
    john = Person("John")
    robert = Person("Robert")
    william = Person("William")
    david = Person("David")
    richard = Person("Richard")
    joseph = Person("Joseph")
    thomas = Person("Thomas")
    charles = Person("Charles")
    christopher = Person("Christopher")
    daniel = Person("Daniel")
    matthew = Person("Matthew")
    anthony = Person("Anthony")
    donald = Person("Donald")
    clark = Person("Clark")
    mark = Person("Mark")
    paul = Person("Paul")
    steven = Person("Steven")
    andrew = Person("Andrew")
    kenneth = Person("Kenneth")
    george = Person("George")
    kevin = Person("Kevin")
    brian = Person("Brian")
    edward = Person("Edward")
    ronald = Person("Ronald")
    timothy = Person("Timothy")
    jason = Person("Jason")
    jeffery = Person("Jeffery")
    jacob = Person("Jacob")
    gary = Person("Gary")
    nicholas = Person("Nicholas")
    eric = Person("Eric")
    stephen = Person("Stephen")
    jonathan = Person("Jonathan")
    larry = Person("Larry")
    justin = Person("Justin")
    scott = Person("Scott")
    anna = Person("Anna")
    nicole = Person("Nicole")

    town1 = Town("Boston")
    town1.add_resident(michael)
    town1.add_resident(jack)
    town1.add_resident(kyle)
    town1.add_resident(annie)
    town1.add_resident(james)
    town1.add_resident(robert)
    town1.add_resident(william)
    town1.add_resident(david)
    town1.add_resident(richard)
    town1.add_resident(joseph)
    town2 = Town("New York City")
    town2.add_resident(max)
    town2.add_resident(charlie)
    town2.add_resident(thomas)
    town2.add_resident(charles)
    town2.add_resident(christopher)
    town2.add_resident(daniel)
    town2.add_resident(matthew)
    town2.add_resident(anthony)
    town2.add_resident(donald)
    town2.add_resident(clark)
    town3 = Town("Baltimore")
    town3.add_resident(alex)
    town3.add_resident(mats)
    town3.add_resident(sami)
    town3.add_resident(ryan)
    town3.add_resident(mark)
    town3.add_resident(paul)
    town3.add_resident(steven)
    town3.add_resident(andrew)
    town3.add_resident(kenneth)
    town3.add_resident(george)
    town4 = Town("LA")
    town4.add_resident(nate)
    town4.add_resident(josh)
    town4.add_resident(kate)
    town4.add_resident(kevin)
    town4.add_resident(brian)
    town4.add_resident(edward)
    town4.add_resident(ronald)
    town4.add_resident(timothy)
    town4.add_resident(nicole)
    town4.add_resident(anna)
    town5 = Town("Chicago")
    town5.add_resident(jason)
    town5.add_resident(jeffery)
    town5.add_resident(gary)
    town5.add_resident(jacob)
    town5.add_resident(nicholas)
    town5.add_resident(eric)
    town5.add_resident(stephen)
    town5.add_resident(jonathan)
    town5.add_resident(larry)
    town5.add_resident(justin)
    town5.add_resident(scott)

    countryB = CountryB("USA")
    countryB.add_town(town1)
    countryB.add_town(town2)
    countryB.add_town(town3)
    countryB.add_town(town4)
    countryB.add_town(town5)

    max.add_friend(jack)
    max.add_friend(kyle)
    max.add_friend(charlie)
    max.add_friend(larry)
    max.add_friend(kevin)
    max.add_friend(nicole)
    max.add_family(kenneth)
    max.add_family(clark)
    max.add_family(james)
    max.add_family(robert)
    jack.add_friend(michael)
    jack.add_friend(annie)
    jack.add_friend(eric)
    jack.add_friend(paul)
    sami.add_friend(max)
    sami.add_friend(ryan)
    sami.add_friend(scott)
    sami.add_friend(ronald)
    sami.add_friend(charlie)
    sami.add_family(thomas)
    sami.add_family(william)
    ryan.add_friend(annie)
    ryan.add_friend(brian)
    ryan.add_friend(daniel)
    ryan.add_family(mats)
    ryan.add_friend(nate)
    mats.add_friend(annie)
    mats.add_friend(max)
    mats.add_friend(kyle)
    mats.add_friend(william)
    nate.add_friend(jack)
    nate.add_friend(michael)
    nate.add_family(anna)
    josh.add_friend(jack)
    josh.add_friend(richard)
    josh.add_family(gary)
    christopher.add_friend(scott)
    christopher.add_family(james)
    christopher.add_family(kenneth)
    mark.add_friend(max)
    mark.add_friend(nicole)
    mark.add_friend(larry)
    eric.add_friend(andrew)
    eric.add_friend(donald)
    eric.add_family(ronald)
    kate.add_friend(nate)
    kate.add_friend(jason)
    kate.add_friend(jeffery)
    kate.add_family(anna)
    larry.add_friend(kyle)
    larry.add_friend(ryan)
    larry.add_family(jonathan)
    anthony.add_friend(max)
    anthony.add_friend(alex)
    anthony.add_friend(david)
    anthony.add_family(richard)
    steven.add_friend(nate)
    steven.add_friend(kevin)
    steven.add_friend(brian)
    steven.add_family(edward)
    steven.add_family(kate)

    # josh.infection = 5
    # josh.set_dead()

    # print(countryB.get_citizens())
    # print(countryB.citizens)
    # list=[]
    # list2=[]
    # for each in countryB.citizens:
    # list2.append(each)
    # list.append(each.rel_scale)
    # print(list)
    # print(list2)

    countryA = CountryA("USSR")
    countryA.distribute_disease_at_very_first(countryB)

    # countryB.check_if_distribute_a()

    # for town in countryB.towns:
    # town.check_if_quarantine()
    # town.check_if_distribute_v()

    # for person in countryB.citizens:
    # person.check_if_dead()

    # print("Test case antidote distribution:")
    # countryB.distributeA = True
    # countryB.distribute_antidote()
    # list3 = []
    # for each in countryB.citizens:
    # list3.append(each.antidote)
    # print(list3)
    # print(jack.antidote)
    # print(annie.antidote)
    # print(max.antidote)
    # print(michael.antidote)

    # print("Test case for vaccine distribution:")
    # town1.distributeV = True
    # town1.distribute_vaccine()
    # list4 = []
    # for each in countryB.citizens:
    # list4.append(each.vaccine)
    # print(list4)
    # print(jack.vaccine)
    # print(michael.vaccine)
    # print(kyle.vaccine)
    # print(annie.vaccine)

    # print(countryB.citizens)
    # print(len(countryB.citizens))
    # data = Global(countryB, 2)

    # day = Day(0)
    # for i in range(int(data.day)):
    # i = 0
    # day.a_day_pass(countryB)
    # i += 1

    day = Day(0) #create day class
    data = Global(countryB, k, day) #create global data collecter
    master = [data.get_infected_rate_country(countryB), data.get_infected_rate_town(), data.get_vaccine_rate(countryB)]
    return master #collect information for GUI
