import logging

from jyotisha import names

from jyotisha.panchaanga import temporal
from jyotisha.panchaanga.temporal import zodiac, PanchaangaApplier
from jyotisha.panchaanga.temporal.hour import Hour


TYAJYA_SPANS_REL = [51, 25, 31, 41, 15, 22, 31, 21, 33,
                    31, 21, 19, 22, 21, 15, 15, 11, 15,
                    57, 25, 21, 11, 11, 19, 17, 25, 31]
AMRITA_SPANS_REL = [43, 49, 55, 53, 39, 36, 55, 45, 57,
                    55, 45, 43, 46, 45, 39, 39, 35, 39,
                    45, 49, 45, 35, 35, 43, 41, 49, 55]
AMRITADI_YOGA = [[None, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 2, 2, 0, 1, 0, 0, 2, 1, 1, 0, 0],
                 [None, 1, 1, 2, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 2, 0, 1, 1, 2, 1, 1],
                 [None, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 2, 2, 0, 1],
                 [None, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 1, 2, 1, 0, 1, 2],
                 [None, 0, 1, 2, 2, 2, 2, 0, 0, 1, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
                 [None, 0, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 0, 1, 1, 1, 1, 2, 0, 1, 1, 2, 1, 1, 1, 1, 0],
                 [None, 1, 1, 0, 0, 1, 1, 1, 1, 2, 0, 1, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 2]]
AMRITADI_YOGA_NAMES = {1: 'siddha', 0: 'amRta', 2: 'maraNa'}
for i in range(7):
  AMRITADI_YOGA[i] = [AMRITADI_YOGA_NAMES.get(n, n) for n in AMRITADI_YOGA[i]]


class NakshatraAssigner(PanchaangaApplier):
  def calc_nakshatra_tyaajya(self, debug=False):
    self.panchaanga.tyajyam_data = [[] for _x in range(self.panchaanga.duration + 1)]
    if self.panchaanga.nakshatram_data[0] is None:
      self.panchaanga.nakshatram_data[0] = zodiac.get_angam_data(self.panchaanga.jd_sunrise[0], self.panchaanga.jd_sunrise[1],
                                                                 zodiac.AngaType.NAKSHATRA, ayanamsha_id=self.panchaanga.ayanamsha_id)
    for d in range(1, self.panchaanga.duration + 1):
      [y, m, dt, t] = temporal.jd_to_utc_gregorian(self.panchaanga.jd_start + d - 1)
      jd = self.panchaanga.jd_midnight[d]
      t_start = self.panchaanga.nakshatram_data[d - 1][-1][1]
      if t_start is not None:
        n, t_end = self.panchaanga.nakshatram_data[d][0]
        if t_end is None:
          t_end = self.panchaanga.nakshatram_data[d + 1][0][1]
        tyaajya_start = t_start + (t_end - t_start) / 60 * (TYAJYA_SPANS_REL[n - 1] - 1)
        tyaajya_end = t_start + (t_end - t_start) / 60 * (TYAJYA_SPANS_REL[n - 1] + 3)
        if tyaajya_start < self.panchaanga.jd_sunrise[d]:
          self.panchaanga.tyajyam_data[d - 1] += [(tyaajya_start, tyaajya_end)]
          if debug:
            logging.debug('![%3d]%04d-%02d-%02d: %s (>>%s), %s–%s' %
                          (d - 1, y, m, dt - 1, names.NAMES['NAKSHATRAM_NAMES']['hk'][n],
                           Hour(24 * (t_end - self.panchaanga.jd_midnight[d - 1])).toString(format='hh:mm*'),
                           Hour(24 * (tyaajya_start - self.panchaanga.jd_midnight[d - 1])).toString(format='hh:mm*'),
                           Hour(24 * (tyaajya_end - self.panchaanga.jd_midnight[d - 1])).toString(format='hh:mm*')))
        else:
          self.panchaanga.tyajyam_data[d] = [(tyaajya_start, tyaajya_end)]
          if debug:
            logging.debug(' [%3d]%04d-%02d-%02d: %s (>>%s), %s–%s' %
                          (d, y, m, dt, names.NAMES['NAKSHATRAM_NAMES']['hk'][n],
                           Hour(24 * (t_end - jd)).toString(format='hh:mm*'),
                           Hour(24 * (tyaajya_start - jd)).toString(format='hh:mm*'),
                           Hour(24 * (tyaajya_end - jd)).toString(format='hh:mm*')))
  
      if len(self.panchaanga.nakshatram_data[d]) == 2:
        t_start = t_end
        n2, t_end = self.panchaanga.nakshatram_data[d][1]
        tyaajya_start = t_start + (t_end - t_start) / 60 * (TYAJYA_SPANS_REL[n2 - 1] - 1)
        tyaajya_end = t_start + (t_end - t_start) / 60 * (TYAJYA_SPANS_REL[n2 - 1] + 3)
        self.panchaanga.tyajyam_data[d] += [(tyaajya_start, tyaajya_end)]
        if debug:
          logging.debug(' [%3d]            %s (>>%s), %s–%s' %
                        (d, names.NAMES['NAKSHATRAM_NAMES']['hk'][n2],
                         Hour(24 * (t_end - jd)).toString(format='hh:mm*'),
                         Hour(24 * (tyaajya_start - jd)).toString(format='hh:mm*'),
                         Hour(24 * (tyaajya_end - jd)).toString(format='hh:mm*')))
  
  def calc_nakshatra_amrta(self, debug=False):
    self.panchaanga.amrita_data = [[] for _x in range(self.panchaanga.duration + 1)]
    if self.panchaanga.nakshatram_data[0] is None:
      self.panchaanga.nakshatram_data[0] = zodiac.get_angam_data(self.panchaanga.jd_sunrise[0], self.panchaanga.jd_sunrise[1],
                                                                 zodiac.AngaType.NAKSHATRA, ayanamsha_id=self.panchaanga.ayanamsha_id)
    for d in range(1, self.panchaanga.duration + 1):
      [y, m, dt, t] = temporal.jd_to_utc_gregorian(self.panchaanga.jd_start + d - 1)
      jd = self.panchaanga.jd_midnight[d]
      t_start = self.panchaanga.nakshatram_data[d - 1][-1][1]
      if t_start is not None:
        n, t_end = self.panchaanga.nakshatram_data[d][0]
        if t_end is None:
          t_end = self.panchaanga.nakshatram_data[d + 1][0][1]
        amrita_start = t_start + (t_end - t_start) / 60 * (AMRITA_SPANS_REL[n - 1] - 1)
        amrita_end = t_start + (t_end - t_start) / 60 * (AMRITA_SPANS_REL[n - 1] + 3)
        if amrita_start < self.panchaanga.jd_sunrise[d]:
          self.panchaanga.amrita_data[d - 1] += [(amrita_start, amrita_end)]
          if debug:
            logging.debug('![%3d]%04d-%02d-%02d: %s (>>%s), %s–%s' %
                          (d - 1, y, m, dt - 1, names.NAMES['NAKSHATRAM_NAMES']['hk'][n],
                           Hour(24 * (t_end - self.panchaanga.jd_midnight[d - 1])).toString(format='hh:mm*'),
                           Hour(24 * (amrita_start - self.panchaanga.jd_midnight[d - 1])).toString(format='hh:mm*'),
                           Hour(24 * (amrita_end - self.panchaanga.jd_midnight[d - 1])).toString(format='hh:mm*')))
        else:
          self.panchaanga.amrita_data[d] = [(amrita_start, amrita_end)]
          if debug:
            logging.debug(' [%3d]%04d-%02d-%02d: %s (>>%s), %s–%s' %
                          (d, y, m, dt, names.NAMES['NAKSHATRAM_NAMES']['hk'][n],
                           Hour(24 * (t_end - jd)).toString(format='hh:mm*'),
                           Hour(24 * (amrita_start - jd)).toString(format='hh:mm*'),
                           Hour(24 * (amrita_end - jd)).toString(format='hh:mm*')))
  
      if len(self.panchaanga.nakshatram_data[d]) == 2:
        t_start = t_end
        n2, t_end = self.panchaanga.nakshatram_data[d][1]
        amrita_start = t_start + (t_end - t_start) / 60 * (AMRITA_SPANS_REL[n2 - 1] - 1)
        amrita_end = t_start + (t_end - t_start) / 60 * (AMRITA_SPANS_REL[n2 - 1] + 3)
        self.panchaanga.amrita_data[d] += [(amrita_start, amrita_end)]
        if debug:
          logging.debug(' [%3d]            %s (>>%s), %s–%s' %
                        (d, names.NAMES['NAKSHATRAM_NAMES']['hk'][n2],
                         Hour(24 * (t_end - jd)).toString(format='hh:mm*'),
                         Hour(24 * (amrita_start - jd)).toString(format='hh:mm*'),
                         Hour(24 * (amrita_end - jd)).toString(format='hh:mm*')))

