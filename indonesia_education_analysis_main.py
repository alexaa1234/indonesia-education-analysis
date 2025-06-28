import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from PIL import Image

df = pd.read_excel("Indonesia_education.xlsx")

pd.set_option('display.float_format','{:,.2f}'.format)
pd.set_option('display.max_columns', None)
df = df.rename(columns={"Education Spend /mo (Rp)":"Education Spendings (Rp)"})
df.columns = [col.strip() for col in df.columns]

cols = [
    'Population (2020)',
    'Avg Monthly Income (Rp)',
    'Students Passed AKM Numeracy',
    'Senior High Enrolled (Age 16–18)',
]

for col in cols:
    df[col] = df[col].astype(str).replace(",","", regex = True)
    df[col] = pd.to_numeric(df[col], errors = 'coerce').astype('float64')



df["% Passed AKM"] = (df["Students Passed AKM Numeracy"]/df["Population (2020)"] * 100).round(2)
df["% Passed AKM Display"] = df["% Passed AKM"].astype(str) + "%"


df["% of Income for Education"] = (df["Education Spendings (Rp)"]/df["Avg Monthly Income (Rp)"] * 100).round(2)
df["% of Income for Education Display"] = (df["% of Income for Education"]).astype(str) + "%"

df.set_index("Region")["Education Spendings (Rp)"].plot(kind = 'bar',color = 'blue', title = 'Average Education Spendings per Region' )
plt.ylabel("Spendings (Rp)")
plt.xlabel("Region")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("Average Education Spendings by Region.png")
plt.clf()

df.set_index("Region")["% of Income for Education"].plot(kind = 'bar', color = 'red', title = "Education Spending by Region (as % of Income)")
plt.xlabel("Region")
plt.ylabel("% of Income for Education")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("Education Spending by Region (as % of Income)")
plt.clf()


#Education priority level pie chart
def education_priority(pct):
    if pct >= 6.57:
        return "High Priority"
    elif pct >= 6.25:
        return "Average Priority"
    else:
        return "Low Priority "

df["Education Priority Level"] = df ["% of Income for Education"].apply(education_priority)
grouped = df.groupby("Education Priority Level")["Region"].apply(lambda x: ", ".join(x)).reset_index()


priority_counts = df["Education Priority Level"].value_counts()
grouped = grouped.set_index("Education Priority Level").loc[priority_counts.index]
labels = [f"{priority}\n" + '\n'.join(regions.split(', ')) for priority, regions in zip(grouped.index,grouped["Region"])]
plt.pie(priority_counts, labels = labels, autopct = "%1.2f%%", colors = ['green','red','yellow'] , startangle = 142)
plt.title("Education Priority Level per Region")
plt.tight_layout()
plt.axis('equal')
#plt.savefig("Education Priority Level per Region.png")
plt.clf()

df.set_index("Region")["Students Passed AKM Numeracy"].plot(kind = 'bar',color = 'orchid', title = 'Number of Students Passed AKM Numeracy by Region' )

ax = plt.gca()
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

plt.ylabel("Number of Students Passed AKM Numeracy")
plt.xlabel("Region")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig('Students Passed AKM Numeracy by Region.png')
plt.clf()

df.set_index("Region")["% Passed AKM"].plot(kind = 'bar', color = 'purple', title = 'Number of Students Passed AKM Numeracy by Region' + '\n' + '(as % of Population)')
plt.xlabel('Region')
plt.ylabel('% Passed AKM')
plt.tight_layout()
plt.xticks(rotation = 45)
plt.savefig('Number of Students Passed AKM Numeracy by Region (as % of Population)')

#Streamlit user interface design
#page set up
st.set_page_config(page_title = "An Analysis on Indonesia's Education System", page_icon = "🎓", layout = 'wide')

#background color
st.markdown(
    """
    <style>
        .stApp {
            background-color: #fffde7
        }
        </style>
    """,
    unsafe_allow_html= True
)

#image border
st.markdown(
    """
    <style> 
        img {
            border: 12px solid #002366;
        }
    </style>
    """,
    unsafe_allow_html= True
)
#title
st.markdown("""
            <div style='text-align: center; background-color: #add8e6; border-radius: 0 0 12px 12px; '>
                <h1 style='
                    color: #000000;
                    font-weight: bold;
                    font-size: 40px
                '>
                    🎓 Indonesia's Education System: Dashboard Analysis
                </h1>
            </div>
         """,
         unsafe_allow_html = True

         )
st.markdown("<h2 style = 'color: black'> Explores a range of dashboards that display key education statistics in regions across Indonesia. </h2>",unsafe_allow_html = True)

#start of analysis
df = pd.read_excel("Indonesia_education.xlsx")
st.markdown("""<h3> 
                <span style ='
                    background-color: #0492c2;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    🧾 Raw Dataset
                </spam>
            </h3>
            """,
            unsafe_allow_html = True
            )
st.dataframe(df)

st.markdown("""<h3> 
                <span style ='
                    background-color: #0492c2;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    🏫 Is education a priority? In which regions is it the most prioritized?
                </spam>
            </h3>
            """,
            unsafe_allow_html = True
            )


st.markdown("""<h4> 
                <span style ='
                    background-color: #e5f3fd;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    💵 Average Education Spendings per Region
                </spam>
            </h4>
            """,
            unsafe_allow_html = True
            )
image2 = Image.open("Average Education Spendings by Region.png")
st.image(image2, width = 800)

st.markdown("""<h4> 
                <span style ='
                    background-color: #e5f3fd;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    💵 Average Education Spendings by Region based on Income
                </spam>
            </h4>
            """,
            unsafe_allow_html = True
            )
image3 = Image.open("Education Spending by Region (as % of Income).png")
st.image(image3, width = 800)

st.markdown("""<h4> 
                <span style ='
                    background-color: #e5f3fd;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    💵 Education Priority levels per Region
                </spam>
            </h4>
            """,
            unsafe_allow_html = True
            )
image4 = Image.open("Education Priority Level per Region.png")
st.image(image4, width = 800 )

st.markdown("""<h3> 
                <span style ='
                    background-color: #0492c2;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    📖 Does having a higher average income increase student performance
                </spam>
            </h3>
            """,
            unsafe_allow_html = True
            )

st.markdown("""<h4> 
                <span style ='
                    background-color: #e5f3fd;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    👩🏻‍🎓 Number of Students that Passed AKM Numeracy by Region
                </spam>
            </h4>
            """,
            unsafe_allow_html = True
            )
image1 = Image.open("Students Passed AKM Numeracy by Region.png")
st.image(image1,  width = 800)


st.markdown("""<h4> 
                <span style ='
                    background-color: #e5f3fd;
                    padding: 6px 12px;
                    color: #000000;
                '>
                    👩🏻‍🎓 Number of Students Passed AKM Numeracy by Region (as % of Population)
                </spam>
            </h4>
            """,
            unsafe_allow_html = True
            )
image5 = Image.open("Number of Students Passed AKM Numeracy by Region (as % of Population).png")
st.image(image5,  width = 800)

st.markdown("---")
st.markdown(""" <h5 style='
                    color: #000000;
                    font-weight: 'bold
            '>
                Made by Alexa - Powered by Streamlit
            </h5>   
            """,
            unsafe_allow_html = True
            )   







