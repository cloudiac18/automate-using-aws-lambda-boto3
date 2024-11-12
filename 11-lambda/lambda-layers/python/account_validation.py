def validateAcct( acctNo, age ):
    if len(acctNo) ==10 and age >=18:
        return 'PASS'
    else:
        return 'FAIL'