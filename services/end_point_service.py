from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri
from db.models.csv1_model import TerrorAttack, Attack, Location
from sqlalchemy import func
from flask import jsonify, request
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os
#     http://127.0.0.1:5000/terror_csv/avg_casualties_by_location?top5=true


def fatal_attack_service():
    session = create_session(database_uri)
    top_5 = request.args.get('top5', 'false').lower() == 'true'

    # ביצוע JOIN בין טבלת TerrorAttack לטבלת Attack לפי attack_type_id
    query = session.query(
        Attack.attack_type_name,  # שם סוג ההתקפה מתוך טבלת Attack
        func.sum(TerrorAttack.num_of_dead * 2 + TerrorAttack.num_of_casualties).label('total_points')  # חישוב הנפגעים
    ).join(
        Attack, TerrorAttack.attack_type_id == Attack.attack_type_id  # קשר בין ה-ID של סוג ההתקפה בטבלאות השונות
    ).group_by(
        Attack.attack_type_name  # קבוצת הנתונים לפי שם סוג ההתקפה
    ).order_by(
        func.sum(TerrorAttack.num_of_dead * 2 + TerrorAttack.num_of_casualties).desc())  # סידור בסדר יורד לפי הנפגעים  # הגבלת התוצאות ל-5 סוגי התקפות קטלניות ביותר

    if top_5:
        query = query.limit(5)

    results = query.all()

    # הכנת התשובה בפורמט JSON
    # יצירת רשימה של תוצאות שתוחזר כ-JSON
    response_data = [
        {"attack_type": result.attack_type_name, "total_points": result.total_points}
        for result in results
    ]

    # החזרת התשובה בפורמט JSON
    return jsonify(response_data)



def fatal_area_service():
    try:
        session = create_session(database_uri)

        # בדיקת פרמטר מהבקשה
        show_top_5 = request.args.get('top5', 'false').lower() == 'true'

        # שאילתה לבסיס הנתונים
        query = session.query(
            TerrorAttack.region_id,
            Location.latitude,
            Location.longitude,
            (TerrorAttack.num_of_dead * 2 + TerrorAttack.num_of_casualties).label('total_points')
        ).join(
            Location, TerrorAttack.location_id == Location.id
        ).filter(
            TerrorAttack.num_of_dead.isnot(None),
            TerrorAttack.num_of_casualties.isnot(None),
            Location.latitude.isnot(None),
            Location.longitude.isnot(None)
        )

        # יצירת DataFrame מהשאילתה
        results = pd.DataFrame(query.all(), columns=['region_id', 'latitude', 'longitude', 'total_points'])

        if results.empty:
            return jsonify({"status": "error", "message": "No data found"}), 404

        # חישוב ציון כללי לפי אזור
        total_points_by_region = (
            results.groupby('region_id')['total_points']
            .sum()
            .reset_index()
            .sort_values(by='total_points', ascending=False)
        )

        # סינון לפי טופ 5 אם המשתמש ביקש
        if show_top_5:
            total_points_by_region = total_points_by_region.head(5)

        # יצירת מפה
        map_center = [results['latitude'].mean(), results['longitude'].mean()]
        folium_map = folium.Map(location=map_center, zoom_start=2)

        # יצירת Cluster
        marker_cluster = MarkerCluster().add_to(folium_map)

        # הוספת מיקומים למפה
        for region_id in total_points_by_region['region_id']:
            region_data = results[results['region_id'] == region_id]
            for _, row in region_data.iterrows():
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=row['total_points'] / 10,
                    color='red',
                    fill=True,
                    fill_color='orange',
                    fill_opacity=0.6,
                    popup=f"Region ID: {row['region_id']}<br>Score: {row['total_points']}"
                ).add_to(marker_cluster)

        # שמירת המפה כתור HTML בתיקיית maps
        output_dir = os.path.join(os.getcwd(), 'maps')
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, 'fatal_area_map.html')
        folium_map.save(output_file)

        # החזרת התוצאה בפורמט JSON
        response_data = total_points_by_region.to_dict(orient='records')

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500








