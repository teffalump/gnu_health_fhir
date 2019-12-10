class familyMember:
    contents = [
        {
            "code": "FAMMEMB",
            "display": "member",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "CHILD",
            "display": "child",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "CHLDADOPT",
            "display": "adopted child",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "DAUADOPT",
            "display": "adopted daughter",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SONADOPT",
            "display": "adopted son",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "CHLDFOST",
            "display": "foster child",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "DAUFOST",
            "display": "foster daughter",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SONFOST",
            "display": "foster son",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "DAUC",
            "display": "daughter",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "DAU",
            "display": "natural daughter",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPDAU",
            "display": "stepdaughter",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NCHILD",
            "display": "natural child",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SON",
            "display": "natural son",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {"code": "SONC", "display": "son", "system": "http://hl7.org/fhir/v3/RoleCode"},
        {
            "code": "STPSON",
            "display": "stepson",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPCHLD",
            "display": "step child",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "EXT",
            "display": "extended family member",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "AUNT",
            "display": "aunt",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MAUNT",
            "display": "maternal aunt",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PAUNT",
            "display": "paternal aunt",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "COUSN",
            "display": "cousin",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MCOUSN",
            "display": "maternal cousin",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PCOUSN",
            "display": "paternal cousin",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GGRPRN",
            "display": "great grandparent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GGRFTH",
            "display": "great grandfather",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MGGRFTH",
            "display": "maternal great-grandfather",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PGGRFTH",
            "display": "paternal great-grandfather",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GGRMTH",
            "display": "great grandmother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MGGRMTH",
            "display": "maternal great-grandmother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PGGRMTH",
            "display": "paternal great-grandmother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MGGRPRN",
            "display": "maternal great-grandparent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PGGRPRN",
            "display": "paternal great-grandparent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GRNDCHILD",
            "display": "grandchild",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GRNDDAU",
            "display": "granddaughter",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GRNDSON",
            "display": "grandson",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GRPRN",
            "display": "grandparent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GRFTH",
            "display": "grandfather",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MGRFTH",
            "display": "maternal grandfather",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PGRFTH",
            "display": "paternal grandfather",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GRMTH",
            "display": "grandmother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MGRMTH",
            "display": "maternal grandmother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PGRMTH",
            "display": "paternal grandmother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MGRPRN",
            "display": "maternal grandparent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PGRPRN",
            "display": "paternal grandparent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "INLAW",
            "display": "inlaw",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "CHLDINLAW",
            "display": "child-in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "DAUINLAW",
            "display": "daughter in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SONINLAW",
            "display": "son in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PRNINLAW",
            "display": "parent in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "FTHINLAW",
            "display": "father-in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MTHINLAW",
            "display": "mother-in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SIBINLAW",
            "display": "sibling in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "BROINLAW",
            "display": "brother-in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SISINLAW",
            "display": "sister-in-law",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NIENEPH",
            "display": "niece/nephew",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NEPHEW",
            "display": "nephew",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NIECE",
            "display": "niece",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "UNCLE",
            "display": "uncle",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MUNCLE",
            "display": "maternal uncle",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PUNCLE",
            "display": "paternal uncle",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PRN",
            "display": "parent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "ADOPTP",
            "display": "adoptive parent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "ADOPTF",
            "display": "adoptive father",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "ADOPTM",
            "display": "adoptive mother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "FTH",
            "display": "father",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "FTHFOST",
            "display": "foster father",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NFTH",
            "display": "natural father",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NFTHF",
            "display": "natural father of fetus",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPFTH",
            "display": "stepfather",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MTH",
            "display": "mother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "GESTM",
            "display": "gestational mother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "MTHFOST",
            "display": "foster mother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NMTH",
            "display": "natural mother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NMTHF",
            "display": "natural mother of fetus",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPMTH",
            "display": "stepmother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NPRN",
            "display": "natural parent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "PRNFOST",
            "display": "foster parent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPPRN",
            "display": "step parent",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SIB",
            "display": "sibling",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "BRO",
            "display": "brother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "HBRO",
            "display": "half-brother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NBRO",
            "display": "natural brother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "TWINBRO",
            "display": "twin brother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "FTWINBRO",
            "display": "fraternal twin brother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "ITWINBRO",
            "display": "identical twin brother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPBRO",
            "display": "stepbrother",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "HSIB",
            "display": "half-sibling",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "HSIS",
            "display": "half-sister",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NSIB",
            "display": "natural sibling",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "NSIS",
            "display": "natural sister",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "TWINSIS",
            "display": "twin sister",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "FTWINSIS",
            "display": "fraternal twin sister",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "ITWINSIS",
            "display": "identical twin sister",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "TWIN",
            "display": "twin",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "FTWIN",
            "display": "fraternal twin",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "ITWIN",
            "display": "identical twin",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SIS",
            "display": "sister",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPSIS",
            "display": "stepsister",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "STPSIB",
            "display": "step sibling",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SIGOTHR",
            "display": "significant other",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "DOMPART",
            "display": "domestic partner",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "SPS",
            "display": "spouse",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "HUSB",
            "display": "husband",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
        {
            "code": "WIFE",
            "display": "wife",
            "system": "http://hl7.org/fhir/v3/RoleCode",
        },
    ]


__all__ = ["familyMember"]
