import math
import argparse


def plural(nb, word):
    if nb == 0:
        return ''
    elif nb > 1:
        return f"{nb} {word}s"
    else:
        return f"{nb} {word}"


parser = argparse.ArgumentParser(description="Ce programme permet de calculer des prêts bancaires a paiement mensuel"
                                             " fixe et à paiement différenciel")
parser.add_argument("-t", "--type", choices=["annuity", "diff"], help="You need to choose only one from the list.")
parser.add_argument("-D", "--payment")
parser.add_argument("-P", "--principal")
parser.add_argument("-n", "--periods")
parser.add_argument("-i", "--interest")

args = parser.parse_args()

if args.type is not None and args.type not in ['annuity', 'diff']:
    print("Incorrect parameters ")
elif args.type == 'diff' and args.payment is not None:
    print("Incorrect parameters")
elif args.interest is None or float(args.interest) < 0:
    print("Incorrect parameters")
elif args.payment is not None and float(args.payment) < 0:
    print("Incorrect parameters")
elif args.principal is not None and float(args.principal) < 0:
    print("Incorrect parameters")
elif args.periods is not None and float(args.periods) < 0:
    print("Incorrect parameters")

elif args.type == 'diff':
    P = float(args.principal)
    i = float(args.interest) / (12 * 100)
    n = int(args.periods)
    GT = 0
    for m in range(n):
        m = m + 1
        Dm = math.ceil(P / n + i * (P - (P * (m - 1)) / n))
        GT = GT + Dm
        print(f"Month {m}: payment is {Dm}")
    print()
    print("Overpayment = {}".format(int(GT - P)))

elif args.type == 'annuity':

    if args.periods is None and args.principal is not None and args.payment is not None:
        loan_princ = float(args.principal)
        month_payment = int(args.payment)
        interest = float(args.interest) / (12 * 100)

        period = math.ceil(math.log(month_payment / (month_payment - interest * loan_princ), 1 + interest))
        nb_year = 0
        nb_month = 0

        if period > 12:
            nb_year = period // 12
            nb_month = period % 12

        if nb_year > 0:
            if nb_month:
                print("It will take {} and {} to repay this loan!".format(plural(nb_year, 'year'), plural(nb_month, 'month')))
            else:
                print("It will take {} to repay this loan!".format(plural(nb_year, 'year')))
        else:
            print("It will take {} to repay this loan!".format(plural(nb_month, 'month')))

        print()
        print("Overpayment = {}".format(int(period * month_payment - loan_princ)))

    elif args.payment is None and args.principal is not None and args.periods is not None:
        loan_princ = float(args.principal)
        nb_month = int(args.periods)
        interest = float(args.interest) / (12 * 100)

        month_payment = math.ceil(loan_princ * interest * (1 + interest) ** nb_month / ((1 + interest) ** nb_month - 1))

        print(f"Your annuily payment = {month_payment}!")
        print()
        print("Overpayment = {}".format(int(month_payment * nb_month - loan_princ)))

    elif args.principal is None and args.payment is not None and args.periods is not None:
        month_payment = int(args.payment)
        nb_month = int(args.periods)
        interest = float(args.interest) / (12 * 100)

        loan_princ = math.floor(month_payment / (interest * (1 + interest) ** nb_month / ((1 + interest) ** nb_month - 1)))

        print(f"Your loan principal = {loan_princ}!")
        print()
        print("Overpayment = {}".format(nb_month * month_payment - loan_princ))

    else:
        print("Incorrect parameters.")
else:
    print("Incorrect parameters.")
