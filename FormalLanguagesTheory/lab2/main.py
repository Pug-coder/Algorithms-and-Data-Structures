from epsilon_deletion import eps_deletion

final = eps_deletion()

for nonterm, value in final.items():
    for val in value:
        print(
            f'{nonterm} -> {val}'
        )
