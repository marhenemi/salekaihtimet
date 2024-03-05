"""
Created: linre-90
Time: 01.03.2024
Updates: 
    - 02.03.2024
"""
from math import ceil, sin, cos, acos, radians, degrees, asin
from datetime import datetime


def calc_sun_rise_n_set(curr_unix_time: float, latitude: float, longitude: float)->tuple[float, float]:
    """
    Sunrise-sunset calculation algorithm. 
    Returns tuple with (sunrise,sunset) in unix epoch timestamp in UTC timezone.
    More info and implementation steps can be found from wikipedia "Complete calculation on Earth".
    https://en.wikipedia.org/wiki/Sunrise_equation
    https://en.wikipedia.org/wiki/Glossary_of_mathematical_symbols
    
    \nCreated: linre-90/01.03.2024
    \nUpdated: linre-90/02.03.2024 - fixed bug in sun declination calculation, there was extra sin() call.
    """
    # calculate julian from unix epoch time
    # 2440587.5 is the julian value of unix jan. 1. 1970
    # 86400.0 is seconds in seconds/d 
    j_date = curr_unix_time / 86400.0 + 2440587.5
    
    # Calculate number of days since Jan 1st, 2000 12:00. 
    # n is the number of days since Jan 1st, 2000 12:00.
    # Formula: n = ceil(j_date - 2451545.0 + 0.0008) 
    n = ceil(j_date - 2451545.0 + 0.0008)
    
    # Calculate Julian mean solar time: j_ms
    # https://en.wikipedia.org/wiki/Solar_time#Mean_solar_time
    # In degrees!
    # Formula: n - longitude/360deg
    j_ms = n - longitude / 360
    
    # Calculate solar Mean anomaly: M
    # M is in degrees!
    # M_Rads is in radians
    # Formula: M = (357.5291 + 0.98560028 * j_ms) mod 360
    M = (357.5291 + 0.98560028 * j_ms) % 360
    M_Rads = radians(M)
    
    # Calculate Equation of center: C
    # https://en.wikipedia.org/wiki/Equation_of_the_center
    # This is needed to calculate next step lambda
    # C is in degrees!
    # Formula: 1.9148 * sin(M) + 0.02 * sin(2 * M) + 0.0003 * sin(3 * M)
    C = 1.9148 * sin(M_Rads) + 0.02 * sin(2 * M_Rads) + 0.0003 * sin(3 * M_Rads)
    
    # Calculate eplictic longtitude: LA
    # https://en.wikipedia.org/wiki/Ecliptic
    # LA is in degrees!
    # LA_Rads is in radians!
    # 102.9372 is a constant for the "argument of perihelion."
    # Formula: LA = (M + C + 180 + 102.9372) mod 360
    LA = (M + C + 180 + 102.9372) % 360
    LA_Rads = radians(LA)
    
    # Calculate solar transit: ST
    # ST is in degrees
    # Formula: ST= 2451545.0 + {mean solar time} + 0.0053 * sin(M) - 0.0069 * sin(2 * LA)
    ST = 2451545.0 + j_ms + 0.0053 * sin(M_Rads) - 0.0069 * sin(2 * LA_Rads)
    
    # Calculate declination of the sun
    # https://en.wikipedia.org/wiki/Declination
    # DS is already a SINner
    # Fixed bug 02.03.2024 there was extra sin taken from DS.
    # Formula: sin DS = sin LA * sin 23.4397
    DS = sin(LA_Rads) * sin(radians(23.4397))
    
    # Calculate hour angle
    # https://en.wikipedia.org/wiki/Hour_angle
    # Not using elevation correction! Eleveatin correction would be added to -.833 sine term
    # with feet: " -1.15 * sqrt(elevation) / 60", meters: -2.076 * sqrt(elevation) / 60
    # Formula: cos HA = ( sin(-0.833) - sin(latitude) * sin(DS) ) / (cos(latitude) * cos(DS))
    try:
        HA = acos(( sin(radians(-0.833)) - sin(radians(latitude)) * DS ) / ( cos(radians(latitude)) * cos(asin(DS)) ))

        # Calulate sun rise and set times
        sunrise = ST - degrees(HA) / 360
        sunset = ST + degrees(HA) / 360

        # return times, convert julian to unix time stamps in UTC
        return ((sunrise - 2440587.5) * 86400, (sunset- 2440587.5) * 86400)
    except ValueError:
        # This mostly happens if sun does not rise at all...
        # return unix time 0, 1.1.1970 midnight
        return (0, 0)


def test(name, latitude, longitude, timestamp, exp_rise, exp_set):
    times = calc_sun_rise_n_set(timestamp, latitude, longitude)
    # Allow 15 minutes movement in rise and set times
    assert abs(times[0] - exp_rise) < 15 * 60, f"{name} failed sun rise: difference is greater thatn 15 minutes. Difference:{abs(exp_rise - times[0])}"
    assert abs(times[1] - exp_set) < 15 * 60, f"{name} failed sun set: difference is greater thatn 15 minutes. Difference:{abs(exp_set - times[1])}"
    print(f"\t Pass: {name}, exp_rise: {exp_rise}, diff_min_rise: {abs(exp_rise - times[0]) / 60}, exp_set:{exp_set}, diff_min_set: {abs(exp_set - times[1])/60}")


if __name__ == "__main__":
    print("\nRunning tests: ")
    
    # Vaasa [63.096, 21.61577] [lat, long]
    test("Vaasa-27.11.2015", 63.096, 21.61577, 1448601248, 1448609280, 1448630040)
    test("Vaasa-13.06.2017", 63.096, 21.61577, 1497327248, 1497313620, 1497386520)
    test("Vaasa-01.03.2024", 63.096, 21.61577, 1709278158, 1709271360, 1709308620)
    test("Vaasa-01.01.2024", 63.096, 21.61577, 1704086048, 1704096600, 1704114240)
    test("Vaasa-03.05.2034", 63.096, 21.61577, 2030242448, 2030234700, 2030295480)
    test("Vaasa-31.12.2034", 63.096, 21.61577, 2051154848, 2051165460, 2051182980)

    # Helsinki [60.192059, 21.61577] [lat, long]
    test("Helsinki-27.11.2015", 60.192059, 24.945831, 1448601248, 1448606880, 1448630820)

    # Nuorgam [70.0833, 27.8500] [lat, long]
    test("Nuorgam-01.01.2024", 70.0833, 27.8500, 1704086048, 0, 0) # expected to get back unix timestamp 0 in cet 2

    # Melborne [70.0833, 27.8500] [lat, long]
    test("Melborne-31.12.2034",-37.840935, 144.946457, 2051154848, 2051118015, 2051171110) # australia is 9 hours ahead... aust times "06:00", "20:45"


    print("\nAll test completed succesfully.")
