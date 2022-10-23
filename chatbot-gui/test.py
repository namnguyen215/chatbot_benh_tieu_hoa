import pandas as pd

data = {
  "calories": [420, 380, 390],
  "Income": [50, 40, 45]
}

df = pd.DataFrame(data)

df.loc[df['Income'] <= 45,"Income"] = 1
print(df)