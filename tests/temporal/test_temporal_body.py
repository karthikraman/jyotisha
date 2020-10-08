import logging

from jyotisha.panchaanga.temporal import body
from jyotisha.panchaanga.temporal.body import Graha, Transit

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)


def test_graha_get_longitude():
  #  13:59:59.99 UT on November 11, 2018
  assert Graha.singleton(Graha.SUN).get_longitude(jd=2458434.083333251) == 229.12286985575702


def test_graha_get_next_raashi_transit():
  from jyotisha.panchaanga.temporal.zodiac import Ayanamsha
  from jyotisha.panchaanga.temporal.zodiac import AngaType
  assert Graha.singleton(Graha.JUPITER).get_transits(jd_start=2457755, jd_end=2458120, anga_type=AngaType.RASHI,
                                                     ayanaamsha_id=Ayanamsha.CHITRA_AT_180) == [
           Transit(body=Graha.JUPITER, jd=2458008.4510242934, anga_type=AngaType.RASHI.name, value_1=6, value_2=7)]
  assert Graha.singleton(Graha.SUN).get_transits(jd_start=2458162.545722, jd_end=2458177.545722, anga_type=AngaType.RASHI, ayanaamsha_id=Ayanamsha.CHITRA_AT_180) == []


def test_get_star_longitude():
  assert body.get_star_longitude(star="Spica", jd=2458434.083333251) == 204.09485939669307
