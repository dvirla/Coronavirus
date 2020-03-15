import CoronaReader
import SARSReader

if __name__=='__main__':
    Chist = CoronaReader.coronareader()
    Chist.recov_death_rates()
    Shist = SARSReader.sarsreader()
    Shist.recov_death_rates()