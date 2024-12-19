import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import func
from io import BytesIO
from flask import Response, request, send_file
from sqlalchemy import extract
from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri
from db.models.csv1_model import TerrorAttack


def get_attack_graphs():
    # שליפת שנה מהפרמטרים של הבקשה
    year = request.args.get('year', type=int)
    session = create_session(database_uri)

    try:
        # מחלץ את השנה והחודש מעמודת date וסופר את כמות ההתקפות
        query = session.query(
            extract('year', TerrorAttack.date).label('year'),
            extract('month', TerrorAttack.date).label('month'),
            func.count(TerrorAttack.id).label('attack_count')
            # מקבץ לפי התאריכים שחולצו
        ).group_by(
            extract('year', TerrorAttack.date),
            extract('month', TerrorAttack.date)
        )

        # אם נשלחה שנה, מוסיף את התנאי לשאילתה כדי להחזיר רק את השנה הזו
        if year:
            query = query.filter(extract('year', TerrorAttack.date) == year)

        #מסדר לפי התאריך
        query = query.order_by(
            extract('year', TerrorAttack.date),
            extract('month', TerrorAttack.date)
        )

        results = query.all()

        # יצירת DataFrame מהנתונים
        data = pd.DataFrame(results, columns=['year', 'month', 'attack_count'])

        # אם לא נשלחה שנה, הצג את כל השנים
        if not year:
            # גרף של תדירות התקפות לפי שנה ומחודש
            data_grouped = data.groupby(['year', 'month']).agg({'attack_count': 'sum'}).reset_index()

            plt.figure(figsize=(10, 6))
            for year_group in data_grouped['year'].unique():
                year_data = data_grouped[data_grouped['year'] == year_group]
                plt.plot(year_data['month'], year_data['attack_count'], marker='o', label=f'Year {year_group}')

            plt.title('Terror Attack Frequency by Month for All Years')
            plt.xlabel('Month')
            plt.ylabel('Number of Attacks')
            plt.xticks(range(1, 13))
            plt.grid(True)
            plt.legend()

            # שמירה של הגרף במשתנה BytesIO
            img_all_years = BytesIO()
            plt.savefig(img_all_years, format='png')
            plt.close()
            #מחזיר את המצביא למקום הראשון, שיתאפשר לקרוא את הקובץ
            img_all_years.seek(0)

            return send_file(img_all_years, mimetype='image/png', as_attachment=False,
                             download_name='all_years_monthly_trend.png')

        # אם נשלחה שנה, הצג את הגרף עבור אותה שנה
        monthly_data = data.groupby(['year', 'month'])['attack_count'].sum().reset_index()
        plt.figure(figsize=(10, 6))
        year_data = monthly_data[monthly_data['year'] == year]  # סינון לפי השנה שנשלחה
        plt.plot(year_data['month'], year_data['attack_count'], marker='o', color='blue')

        plt.title(f'Terror Attack Frequency for {year}')
        plt.xlabel('Month')
        plt.ylabel('Number of Attacks')
        plt.xticks(range(1, 13))
        plt.grid(True)

        # שמירה של הגרף במשתנה BytesIO
        img_month = BytesIO()
        plt.savefig(img_month, format='png')
        plt.close()
        img_month.seek(0)

        return send_file(img_month, mimetype='image/png', as_attachment=False,
                         download_name=f'{year}_monthly_trend.png')

    except Exception as e:
        return {"status": "error", "message": str(e)}