def remaining_balance():
    os_bal = 4800 #input('Enter the outstanding balance on your credit card:')
    apr = .2 #input('Enter the annual credit card interest rate as a decimal:')
    min_pr = .02 #input('Enter the minimum monthly payment rate as a decimal:')
    mpr = apr / 12

    tot_paid = 0

    for i in range(1, 13):
        min_payment = float(min_pr) * float(os_bal)

        interest_paid = mpr * float(os_bal)

        principal_paid = min_payment - interest_paid

        os_bal -= principal_paid

        tot_paid += min_payment



        print 'Month:', i

        print 'Minimum Monthly Payment:', round(min_payment, 2)

        print 'Principal paid:', round(principal_paid, 2)

        print 'Remaining balance:', round(os_bal,2)

    print 'RESULT'

    print 'Total Amount Paid:', round(tot_paid,2)

    print 'Remaining Balance:', round(os_bal,2)

remaining_balance()







