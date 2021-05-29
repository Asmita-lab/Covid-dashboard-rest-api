class CovidData(object):
    def __init__(self, country_name, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases,
                 serious_critical, total_tests, population):
        self.country_name = country_name
        self.total_cases = total_cases
        self.new_cases = new_cases
        self.total_deaths = total_deaths
        self.new_deaths = new_deaths
        self.total_recovered = total_recovered
        self.active_cases = active_cases
        self.serious_critical = serious_critical
        self.total_tests = total_tests
        self.population = population
        if total_recovered is not '' and total_cases is not '':
            self.recovery_rate = str(
                round(int(total_recovered.replace(',', '')) / int(total_cases.replace(',', '')), 2))
        else:
            self.recovery_rate = 0
        if total_cases is not '' and population is not '':
            self.percentage_of_population_infected = str(round(int(total_cases.replace(',', '')) / int(
                population.replace(',', '')), 2))
        else:
            self.percentage_of_population_infected = 0