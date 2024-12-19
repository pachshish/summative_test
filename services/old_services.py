from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri
from db.models.csv1_model import Location, TerrorAttack
from flask import jsonify, request
from sqlalchemy import func



def fatal_area_service():
    session = create_session(database_uri)

    # בדיקת פרמטר הטופ 5 מהבקשה
    top_5 = request.args.get('top5', 'false').lower() == 'true'

    query = session.query(
        Location.latitude,
        Location.longitude,
        func.avg(TerrorAttack.num_of_dead * 2 + TerrorAttack.num_of_casualties).label('avg_points')
    ).join(
        TerrorAttack, TerrorAttack.location_id == Location.id
    ).group_by(
        Location.latitude, Location.longitude
    ).order_by(
        func.avg(TerrorAttack.num_of_dead * 2 + TerrorAttack.num_of_casualties).desc()
    )

    # הוספת הגבלת טופ 5 אם המשתמש ביקש
    if top_5:
        query = query.limit(5)

    results = query.all()

    # הכנת התשובה בפורמט JSON
    response_data = [
        {"latitude": result.latitude, "longitude": result.longitude, "avg_points": round(result.avg_points, 2)}
        for result in results
    ]

    return jsonify(response_data)
