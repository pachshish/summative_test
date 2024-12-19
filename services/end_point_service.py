from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri
from db.models.csv1_model import TerrorAttack, Attack
from sqlalchemy import func
from flask import jsonify, request

import folium


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





def top_5_groups_with_casualties_service():
    try:
        session = create_session(database_uri)


        query = session.query(
            TerrorAttack.group_name,
            func.sum(TerrorAttack.num_of_dead * 2 + TerrorAttack.num_of_casualties).label('total_points')
        ).group_by(
            TerrorAttack.group_name
        ).order_by(
            func.sum(TerrorAttack.num_of_dead * 2 + TerrorAttack.num_of_casualties).desc()
        ).limit(5)

        response_data = [
            {"group_name": result.group_name, "total_points": result.total_points}
            for result in query
        ]

        return jsonify(response_data)
    except Exception as e:
        return {"status": "error", "message": str(e)}










