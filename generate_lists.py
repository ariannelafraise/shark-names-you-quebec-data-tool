import pandas

GENDERS = ('GIRL', 'BOY', 'BOTH')
NUMBER_OF_NAMES = 1200

DONNEES_QUEBEC_GIRLS_FILE_PATH = 'donnees_quebec/filles1980-2023.csv'
DONNEES_QUEBEC_BOYS_FILE_PATH = 'donnees_quebec/gars1980-2023.csv'

GIRLS_NAMES_FILE_PATH = 'data/girl_names.csv'
BOYS_NAMES_FILE_PATH = 'data/boy_names.csv'
BOTH_NAMES_FILE_PATH = 'data/both_names.csv'

OLD_COL_NAME_GIRLS = 'Prenom_feminin'
OLD_COL_NAME_BOYS = 'Prenom_masculin'
NEW_COL_NAME = 'Name'


def generate_lists():
    print('Generating lists ...\n')
    generate_list('GIRL')
    print(f"'{GIRLS_NAMES_FILE_PATH}' generated.")
    generate_list('BOY')
    print(f"'{BOYS_NAMES_FILE_PATH}' generated.")
    generate_list('BOTH')
    print(f"'{BOTH_NAMES_FILE_PATH}' generated.")
    print('\nDone!')


def generate_list(gender):
    if gender not in GENDERS:
        raise ValueError('gender is not valid.')

    match gender:
        case 'GIRL':
            df = get_data(gender)
            filtered_df = filter_data(df, gender)
            filtered_df.to_csv(GIRLS_NAMES_FILE_PATH)

        case 'BOY':
            df = get_data(gender)
            filtered_df = filter_data(df, gender)
            filtered_df.to_csv(BOYS_NAMES_FILE_PATH)

        case 'BOTH':
            df1, df2 = get_data(gender)
            filtered_df = filter_data((df1, df2), gender)
            filtered_df.to_csv(BOTH_NAMES_FILE_PATH)

    return 0


def get_data(gender):
    match gender:
        case 'GIRL':
            return pandas.read_csv(
                DONNEES_QUEBEC_GIRLS_FILE_PATH, usecols=[OLD_COL_NAME_GIRLS, 'Total']
            )
        case 'BOY':
            return pandas.read_csv(
                DONNEES_QUEBEC_BOYS_FILE_PATH, usecols=[OLD_COL_NAME_BOYS, 'Total']
            )
        case 'BOTH':
            return (
                pandas.read_csv(
                    DONNEES_QUEBEC_GIRLS_FILE_PATH, usecols=[OLD_COL_NAME_GIRLS, 'Total']
                ),
                pandas.read_csv(
                    DONNEES_QUEBEC_BOYS_FILE_PATH, usecols=[OLD_COL_NAME_BOYS, 'Total']
                )
            )


def filter_data(df, gender):
    # Params:
    # either:
    # df, 'GIRL' or 'BOY
    # or
    # (girl_df, boy_df), 'BOTH'

    # Drop duplicate names,
    # sort from most popular to least popular,
    # select {NUMBER_OF_NAMES} names,
    # rename column Prenom_XXX to Name
    col = None
    match gender:
        case 'GIRL':
            col = OLD_COL_NAME_GIRLS
        case 'BOY':
            col = OLD_COL_NAME_BOYS
        case 'BOTH':
            if type(df) is not tuple:
                raise ValueError('df should be a tuple.')

            girl_df = filter_data(df[0], 'GIRL')
            boy_df = filter_data(df[1], 'BOY')
            both_df = pandas.concat([girl_df, boy_df])
            # Sorts twice, to make sure the duplicate that is kept is the one with the highest total.
            # Could be improved to
            both_df = both_df.groupby(both_df.index).sum().sort_values(by=['Total'], ascending=False)
            return both_df

    df = df.rename(columns={col: NEW_COL_NAME})
    df = df.set_index(NEW_COL_NAME)

    df = df.groupby(df.index).sum()

    df = df.sort_values(by=['Total'], ascending=False).head(NUMBER_OF_NAMES)

    # Drop first row (it's not an actual name, just a sum)
    df = df.iloc[1:, :]

    return df


if __name__ == '__main__':
    generate_lists()
