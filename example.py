import argparse
import json
from fast_flights import FlightData, Passengers, create_filter, get_flights

def flight_to_dict(flight):
    return {
        "is_best": getattr(flight, 'is_best', None),
        "name": getattr(flight, 'name', None),
        "departure": getattr(flight, 'departure', None),
        "arrival": getattr(flight, 'arrival', None),
        "arrival_time_ahead": getattr(flight, 'arrival_time_ahead', None),
        "duration": getattr(flight, 'duration', None),
        "stops": getattr(flight, 'stops', None),
        "delay": getattr(flight, 'delay', None),
        "price": getattr(flight, 'price', None),
    }

def result_to_dict(result):
    return {
        "current_price": getattr(result, 'current_price', None),
        "flights": [flight_to_dict(flight) for flight in getattr(result, 'flights', [])]
    }

def main():
    # Argument parser for command-line input
    # parser = argparse.ArgumentParser(description="Flight Price Finder")
    # parser.add_argument('--origin', required=True, help="Origin airport code")
    # parser.add_argument('--destination', required=True, help="Destination airport code")
    # parser.add_argument('--depart_date', required=True, help="Beginning trip date (YYYY-MM-DD)")
    # parser.add_argument('--return_date', required=True, help="Ending trip date (YYYY-MM-DD)")
    # parser.add_argument('--adults', type=int, default=1, help="Number of adult passengers")
    # parser.add_argument('--type', type=str, default="economy", help="Fare class (economy, premium-economy, business or first)")
    # parser.add_argument('--max_stops', type=int, help="Maximum number of stops (optional, [0|1|2])")
    # parser.add_argument('--inject_eu_cookies', action=argparse.BooleanOptionalAction, help="Cookies to bypass EU data collection form")


    # args = parser.parse_args()

    # Create a new filter
    filter = create_filter(
        flight_data=[
            FlightData(
                date="2025-04-01",  # Date of departure for outbound flight
                from_airport="YUL",
                to_airport="MIA"
            )
        ],
        trip="one-way",  # Trip (round-trip, one-way)
        seat="economy",  # Seat (economy, premium-economy, business or first)
        passengers=Passengers(
            adults=1,
            children=0,
            infants_in_seat=0,
            infants_on_lap=0
        ),
        max_stops=2
    )

    b64 = filter.as_b64().decode('utf-8')
    print(
        "https://www.google.com/travel/flights?tfs=%s" % b64
    )

    # Get flights with the filter
    result = get_flights(
        flight_data=[
            FlightData(
                date="2025-04-03", 
                from_airport="YUL", 
                to_airport="FLL"
            )
        ],
        trip="round-trip",
        seat="economy",
        passengers=Passengers(
            adults=1, 
            children=0,
            infants_in_seat=0, 
            infants_on_lap=0
        ),
        currency="CAD"
    )

    try:
        # Manually convert the result to a dictionary before serialization
        result_dict = result_to_dict(result)
        print(json.dumps(result_dict, indent=4))
    except TypeError as e:
        print("Serialization to JSON failed. Raw result output:")
        print(result)
        print("Error details:", str(e))

    # Print price information
    print("The price is currently", result.current_price)

if __name__ == "__main__":
    main()
