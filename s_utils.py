"""
Created: linre-90
Time: 01.03.2024
Updates: 
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
    \n
    NOTE: This function is most accurate on [lat:0, long: 0]. Time errors grow depending on latitude, longitude change.
    In finland the error is roughly in 0-15 min in 20 years span. New york and Australia time errors are somewhere around 1h.
    \n
    \nCreated: linre-90/01.03.2024
    \nUpdated:
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
    # Formula: sin DS = sin LA * sin 23.4397
    DS = sin(sin(LA_Rads) * sin(radians(23.4397)))
    
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
    result_rise = datetime.fromtimestamp(times[0])
    result_set = datetime.fromtimestamp(times[1])
    expected_rise = datetime.strptime(exp_rise, "%H:%M")
    expected_set = datetime.strptime(exp_set, "%H:%M")
    
    # hour difference should always be 0
    assert abs(result_rise.hour - expected_rise.hour) == 0, f"{name} failed sun rise: hour difference not zero. Difference:{abs(result_rise.hour - expected_rise.hour)}"
    assert abs(result_rise.minute - expected_rise.minute) <= 15, f"{name} failed sun rise: minute difference bigger than 15. Difference:{abs(result_rise.minute - expected_rise.minute)}"
    # allow 15 min difference in all tests
    assert abs(expected_set.hour - result_set.hour) == 0, f"{name} failed sun set: hour difference not zero. Difference:{abs(expected_set.hour - result_set.hour)}"
    assert abs(result_set.minute - expected_set.minute) <= 15, f"{name} failed sun set: minute difference bigger than 15. Difference:{abs(result_set.minute - expected_set.minute)}"

    print(f"\t Pass: {name}, rise: {exp_rise}, diff_min: {abs(expected_rise.minute - result_rise.minute)}, set:{exp_set}, diff_min: {abs(expected_set.minute - result_set.minute)}")


if __name__ == "__main__":
    print("\nRunning tests: ")

    # Vaasa [63.096, 21.61577] [lat, long]
    test("Vaasa-27.11.2015", 63.096, 21.61577, 1448601248, "9:28", "15:14")
    test("Vaasa-13.06.2017", 63.096, 21.61577, 1497327248, "3:27", "23:42")
    test("Vaasa-01.03.2024", 63.096, 21.61577, 1709278158, "7:36", "17:57")
    test("Vaasa-01.01.2024", 63.096, 21.61577, 1704086048, "10:10", "15:04")
    test("Vaasa-03.05.2034", 63.096, 21.61577, 2030242448, "5:05", "21:58")
    test("Vaasa-31.12.2034", 63.096, 21.61577, 2051154848, "10:11", "15:03")

    # Helsinki [60.192059, 21.61577] [lat, long]
    test("Helsinki-27.11.2015", 60.192059, 24.945831, 1448601248, "8:48", "15:27")

    # Nuorgam [70.0833, 27.8500] [lat, long]
    test("Nuorgam-01.01.2024", 70.0833, 27.8500, 1704086048, "2:00", "2:00") # expected to get back unix timestamp 0 in cet 2

    # Center of the world [0, 0] [lat, long]
    test("Center-01.01.2024", 0, 0, 1704086048, "07:59", "20:07") # input time is in CET


    print("\nAll test completed succesfully.")
