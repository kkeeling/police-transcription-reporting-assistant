# TASK

Based on the following audio transcription, generate a police report:

**Transcription:**

```
{transcription}
```

The user has requested a **{reportType}**. Based on this selection, you will generate the appropriate report using only facts from the transcript. Utilize appropriate law enforcement terminology and formatting conventions for the chosen report type.

Follow these guidelines when creating the report:

1. Maintain a neutral, impartial tone throughout.
2. Concentrate on key information such as dates, times, locations, individuals involved, and the sequence of events.
3. For any ambiguities, note them without speculation.
4. If information is missing or unclear, state "Information not provided in transcript" rather than making assumptions.
5. Use the following structure to present the report:

## REPORT FORMAT

**Officer full name and badge number:**

**Occurrence number:**

**Occurrence type:**

**Report Time (Dispatch time):**

**Occurrence Time:**

**Persons Details:**

- **Surname:**
- **Given 1:**
- **Given 2:**
- **Sex type:**
- **Date of Birth:**
- **Persons Address:**
  - **House or building number:**
  - **Street Address:**
  - **Apartment or room number:**
  - **City, Town:** (if not a Thunder Bay address)
  - **Type of Residence:** (Business Checks, Frequents, Observed Residence, Temporary Residence)
- **Contact info:**
  - **Phone number including area code:**
  - **Phone # Type:** (cell, home, work)
  - **Social Media Type:** (Facebook, Snapchat, Instagram, etc.)
  - **Social Media Handle:**
  - **Email address:**
- **Involvement type:** [Examples - Arrested, Accused, Attending Physician, Complainant, Coroner, Cyclist, Deceased, Emergency Services, Escapee, Finder, Injured, Located, Mental Health, Missing, Observed, Owner, Paramedic, Pedestrian, Reporter, Street Checked, Suicidal, Suspect, Vehicle Driver, Vehicle Passenger, Victim, Wanted, Warned, Witness]

**Narrative:**
[Include the narrative according to the Report Writing Standards. Do not use point form.]

**End of Report**

**Badge Number:** [Your badge number] - **Date and Time:** [Current date and time]

## REPORT EXAMPLE

```
{example_report}
```

## OUTPUT FORMAT

Remember to adhere to the following Report Writing Standards:

- Use Font: Arial; Size: 2 (if typing in Word – Font: Arial; Size 10)
- Use 24-hour clock for times without colons (e.g., 2146 hours)
- Type all reports in third person
- Start all reports with date, time, and author
- Use proper address order in the report
- Capitalize last names (e.g., John SMITH)
- Do not use police jargon, acronyms, or short forms in the body of the report (exceptions: CPIC, DNA, CFRO)
- For acronyms, spell out the full term on first use, followed by the acronym in parentheses

Be mindful of the sensitive nature of law enforcement reports. Maintain strict confidentiality and objectivity in your analysis. Strive for comprehensiveness, ensuring no relevant details from the transcript are omitted.
