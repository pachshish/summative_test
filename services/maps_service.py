from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri
from db.models.csv1_model import TerrorAttack, Location
from flask import jsonify, request
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from sqlalchemy import func

import os


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
        df = pd.DataFrame(query.all(), columns=['region_id', 'latitude', 'longitude', 'total_points'])

        # חישוב ציון כללי לפי אזור
        total_points_by_region = (
            df.groupby('region_id')['total_points']
            .sum()
            .reset_index()
            .sort_values(by='total_points', ascending=False)
        )

        # סינון לפי טופ 5 אם המשתמש ביקש
        if show_top_5:
            total_points_by_region = total_points_by_region.head(5)

        # יצירת מפה
        map_center = [df['latitude'].mean(), df['longitude'].mean()]
        folium_map = folium.Map(location=map_center, zoom_start=2)

        # יצירת Cluster שמקבץ נקודות קרובות
        marker_cluster = MarkerCluster().add_to(folium_map)

        # הוספת מיקומים למפה
        for region_id in total_points_by_region['region_id']:
            region_data = df[df['region_id'] == region_id]
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



def active_terror_groups_service():
        session = create_session(database_uri)
        region_id = request.args.get('region_id', 'false').lower() == 'true'


        # שאילתה לבסיס הנתונים
        query = session.query(
            TerrorAttack.region_id,
            TerrorAttack.group_name,
            Location.latitude,
            Location.longitude,
            func.count(TerrorAttack.id).label('attack_count')
        ).join(
            Location, TerrorAttack.location_id == Location.id
        ).filter(
            TerrorAttack.group_name.isnot(None),
            Location.latitude.isnot(None),
            Location.longitude.isnot(None)
        ).group_by(
             TerrorAttack.region_id,
             TerrorAttack.group_name,
             Location.latitude,
             Location.longitude
        )

        if region_id:
            query = query.filter(TerrorAttack.region_id == region_id)

        # המרת התוצאות ל-DataFrame
        df = pd.DataFrame(query.all(), columns=['region_id', 'group_name', 'latitude', 'longitude', 'attack_count'])

        # חישוב כמות התקפות לפי קבוצה ואזור
        top_groups_by_region = (
            df.groupby(['region_id', 'group_name'])['attack_count']
            .sum()
            .reset_index()
            .sort_values(by='attack_count', ascending=False)
        )

        # יצירת מפה
        map_center = [df['latitude'].mean(), df['longitude'].mean()]
        folium_map = folium.Map(location=map_center, zoom_start=2)

        # יצירת Cluster של המרקרים
        marker_cluster = MarkerCluster().add_to(folium_map)

        # הוספת נקודות למפה
        for region in top_groups_by_region['region_id'].unique():
            region_data = top_groups_by_region[top_groups_by_region['region_id'] == region]
            most_active_group = region_data.iloc[0]
            group_popup = f"Most Active Group: {most_active_group['group_name']}<br>Total Attacks: {most_active_group['attack_count']}<br><br>Top 5 Groups:<br>"

            for _, row in region_data.head(5).iterrows():
                group_popup += f"{row['group_name']}: {row['attack_count']} attacks<br>"

            region_location = df[df['region_id'] == region].iloc[0]
            folium.Marker(
                location=[region_location['latitude'], region_location['longitude']],
                popup=group_popup
            ).add_to(marker_cluster)

        # שמירת המפה לתיקייה
        output_dir = os.path.join(os.getcwd(), 'maps')
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, 'active_terror_groups_map.html')
        folium_map.save(output_file)

        response_data = top_groups_by_region.to_dict(orient='records')

        return jsonify(response_data)






