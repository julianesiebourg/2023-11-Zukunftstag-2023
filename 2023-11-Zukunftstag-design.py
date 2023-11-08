#!/usr/bin/env python
# coding: utf-8

# # Zukunftstag 2023
# 
# Jitao David Zhang, November 2023

# Wir lernen gemeinsam Jupyter Lab kennen mit eine simulierte klinische Studie. Wir werden die Daten mit Jupyter Notebook analysieren und visualisieren, und die Daten gemeinsam interpretieren.
# 
# Die Code wurde auf [jupyter.org/try-jupyter](https://jupyter.org/try-jupyter) getestet. Man braucht nur eine Web-browser, um das Program durchzuführen.

# ## Sicherstellen, dass Jupyter funktioniert

# In[1]:


3 + 9


# In[2]:


9/3


# In[3]:


my_name = "David"
welcome = "Hello, " + my_name
print(welcome)


# In[4]:


import numpy as np


# In[5]:


my_numbers = range(1, 10)
np.sum(my_numbers)


# In[6]:


my_numbers_2 = range(1, 100)
np.sum(my_numbers_2)


# # Eine klinische Studie simulieren

# In[7]:


import pandas as pd


# In[8]:


np.random.seed(1887)


# In[9]:


names = ["Emma", "Olivia", "Emily", "James", "Daniel",
         "Benjamin", "Michael", "Alexander", "Jacob", "Samuel",
         "Isabella", "Thomas", "Sarah", "Ava", "Charlotte", "Elizabeth",
         "Liam", "Mia", "Ethan", "Ella", "Sophia", "Joshua", "Oliver", "Grace",
         "Anna", "Lena", "Sophia", "Laila", "Emma", "Karl"]
len(names)


# In[10]:


pre_g0 = np.random.normal(8, 1.5, size=10)
post_g0 = np.random.normal(8, 1.5, size=10)
pre_g1 = np.random.normal(8, 1.5, size=10)
post_g1 = np.random.normal(7, 1.5, size=10)
pre_g2 = np.random.normal(8, 1.5, size=10)
post_g2 = np.random.normal(5, 1.5, size=10)
pre_all = np.round(np.clip(np.concatenate((pre_g0, pre_g1, pre_g2), axis=None), 0, 10), 1)
post_all = np.round(np.clip(np.concatenate((post_g0, post_g1, post_g2), axis=None), 0, 10))


# In[11]:


treatments = np.concatenate((["PilleA"] * 10, ["PilleB"] * 10, ["PilleC"] * 10), axis=None)


# In[12]:


trial_data = pd.DataFrame({"Name":names,
                          "Behandlung": treatments,
                          "Vor": pre_all,
                          "Nach": post_all},
                         index=names)


# In[13]:


print(trial_data)


# In[14]:


trial_data.sort_values(by=["Behandlung", "Name"])


# ## Wie kann man eine Liste von Angaben in einer DateFrame umwandeln?

# In[15]:


person1 = ['David', 'PilleA', 4.7, 4.5]
person2 = ['Emma', 'PilleB', 4.5, 4]
person3 = ['Matteo', 'PilleC', 4.5, 4]
person_df = pd.DataFrame([person1, person2, person3],
            columns=['Name', 'Behandlung', 'Vor', 'Nach'])
person_df.index = person_df["Name"].tolist()
person_df


# ## Die Daten mit Abbildungen darstellen

# In[16]:


import matplotlib.style as style
import matplotlib.pyplot as plt
style.use("fast")


# In[17]:


ax = trial_data.plot.bar()
plt.xlabel("Teilnehmer")
plt.ylabel("Schmerzskala")
plt.show()


# In[18]:


ax = trial_data.sort_values(['Behandlung', 'Name']).plot.line(rot=90)
ax.set_xticks(range(len(trial_data['Name'])))
ax.set_xticklabels(trial_data['Name'])
plt.show()


# In[19]:


trial_data.sort_values(by=["Behandlung", "Name"]).plot.bar()


# In[20]:


trial_data.boxplot(column=["Vor", "Nach"], by="Behandlung")
plt.show()


# ## Mit den Daten arbeiten

# In[21]:


trial_data["Unterschied"] = trial_data["Nach"] - trial_data["Vor"]
print(trial_data)


# In[22]:


trial_data.sort_values("Unterschied", ascending=False)


# In[23]:


trial_data.boxplot(column="Unterschied", by="Behandlung", grid=False)
plt.axhline(y=0, color="k", linestyle="--")
trial_data.plot.scatter("Behandlung", "Unterschied")
plt.axhline(y=0, color="k", linestyle="--")
plt.show()


# In[24]:


p = trial_data.boxplot(column="Unterschied", by="Behandlung", grid=False)
plt.axhline(y=0, color="k", linestyle="--")
for b, d in enumerate(trial_data["Unterschied"]):
    behandlung = trial_data["Behandlung"][b]
    if behandlung == "PilleA":
        x = 1
    elif behandlung == "PilleB":
        x = 2
    elif behandlung == "PilleC":
        x = 3
    plt.scatter(x, d, c="blue")
plt.show()


# In[25]:


## density plot is not supported by Jupyter
## trial_pivot = trial_data.reset_index().pivot(columns="Behandlung", values="Unterschied")
## trial_pivot.plot.density()
## plt.axvline(x=0, c="k", linestyle="--")
## plt.show()


# ## Eine kleine statistische Analyse

# In[26]:


import statsmodels as sm
import statsmodels.api as sma
from statsmodels.formula.api import ols


# In[27]:


pille_effect = ols('Unterschied ~ Behandlung', data = trial_data).fit()
print(pille_effect.summary())


# In[28]:


table = sma.stats.anova_lm(pille_effect)
print(table)


# ## Die Daten exportieren

# In[29]:


trial_data[['Behandlung', 'Vor', 'Nach']].to_csv("20231108-simulated-trial-data.tsv", sep="\t", index=False)


# ## Fragen

# 1. Wer glaubt, dass ihre/sein Pille hat funktioniert für sie/ihn? Wer glaubt, dass die Pille nicht funktioniert hat?
# 2. Wenn wir davon ausgehen, dass Pille A, Pille B, Pille C jeweilse Placebo, ein neu Medikament von einer niedriger Dose, und das selbe neue Medikament von einer höheren Dose sind. Welche Schlussfolgerungen können wir ziehen?
# 3. Um das Medikament zu mehr Patienten bringen, worauf müssen wir noch beachten?
# 4. Was können wir noch mit den Daten machen?
