from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    df = pd.read_csv("all_page_ambition_data.csv")
    
    if request.method == 'POST':
        location = request.form.get('location')
        industry = request.form.get('industry')
        rating = request.form.get('rating')
        output = request.form.get('output')
        
        if location:
            df = df[df['Location'].str.contains(location, na=False)]
        if industry:
            df = df[df['Industry'].str.contains(industry, na=False)]
        if rating:
            df = df[df['Rating'] == float(rating)]
        
        if output == 'Show Table':
            return render_template("table_page.html", data=df.to_dict('records'))
        elif output == 'Show Visualizations':
            def parse_number(s):
                if pd.isna(s) or s == '--':
                    return 0
                s = str(s).strip()
                if 'k' in s.lower():
                    return float(s.replace('k', '').replace('K', '')) * 1000
                elif 'l' in s.lower():
                    return float(s.replace('l', '').replace('L', '')) * 100000
                else:
                    return float(s)

            df['Jobs_parsed'] = df['Jobs'].apply(parse_number)
            df['Salery_parsed'] = df['Salery'].apply(parse_number)
            df['Review_parsed'] = df['Review'].apply(parse_number)

            if not os.path.exists('static'):
                os.makedirs('static')

         
            plt.figure(figsize=(8,6))
            top10 = df.nlargest(10, 'Rating')
            plt.bar(top10['Company_Names'], top10['Rating'])
            plt.title('Top 10 Companies by Rating')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('static/graph1.png')
            plt.close()

          
            plt.figure(figsize=(8,6))
            plt.scatter(df['Review_parsed'], df['Rating'])
            plt.title('Rating vs Number of Reviews')
            plt.xlabel('Reviews')
            plt.ylabel('Rating')
            plt.tight_layout()
            plt.savefig('static/graph2.png')
            plt.close()

    
            plt.figure(figsize=(8,6))
            industry_counts = df['Industry'].value_counts()
            plt.pie(industry_counts.values, labels=industry_counts.index, autopct='%1.1f%%')
            plt.title('Industry Distribution')
            plt.tight_layout()
            plt.savefig('static/graph3.png')
            plt.close()

   
            plt.figure(figsize=(8,6))
            plt.hist(df['Rating'], bins=10)
            plt.title('Rating Distribution')
            plt.xlabel('Rating')
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.savefig('static/graph4.png')
            plt.close()

   
            plt.figure(figsize=(8,6))
            avg_rating = df.groupby('Industry')['Rating'].mean().reset_index()
            plt.bar(avg_rating['Industry'], avg_rating['Rating'])
            plt.title('Average Rating by Industry')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('static/graph5.png')
            plt.close()

    
            plt.figure(figsize=(8,6))
            plt.scatter(df['Jobs_parsed'], df['Salery_parsed'])
            plt.title('Jobs vs Salary')
            plt.xlabel('Jobs')
            plt.ylabel('Salary')
            plt.tight_layout()
            plt.savefig('static/graph6.png')
            plt.close()

            graphs = ['graph1.png', 'graph2.png', 'graph3.png', 'graph4.png', 'graph5.png', 'graph6.png']

            return render_template("visualization_page.html", graphs=graphs)
        else:
            return render_template("table_page.html", data=df.to_dict('records'))
    
   
    location = df['Location'].dropna().unique()
    industry = df['Industry'].dropna().unique()
    rating = df['Rating'].dropna().unique()
    
    return render_template("home.html", options=location , options2=industry, options3=rating)




app.run(debug=True , port= 5300)