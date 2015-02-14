def calculate_monthly_payment():
    principal = 999999 #input('Enter the outstanding balance on your credit card:')
    apr = .18 #input('Enter the annual credit card interest rate as a decimal:')

    mpr = apr/12

    low = principal/12

    high = (principal*(1+apr/12)**12)/12

    monthly_payment = (low + high)/2

    paidoff = False

    # Fix the payment and keep adding 10 till os_bal becomes less than or equal to 0.
    while not paidoff:
        monthly_payment += 0.001

        months = 0

        os_bal = principal

        # Counting the number of months to pay off the loan with a fixed payment.
        while months < 12 and os_bal > 0:

            months += 1

            os_bal = float(os_bal*(1+mpr) - monthly_payment)


        if os_bal <= 0:

            paidoff = True

    print 'Monthly payment to pay off debt in 1 year:', monthly_payment

    print 'Number of months needed:' , months

    print 'balance:', round(os_bal, 2)

calculate_monthly_payment()