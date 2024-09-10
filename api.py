from flask import Flask, request, jsonify
from database import Database

app = Flask(__name__)

@app.route('/poarta/json', methods=['POST'])
def receive_json():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    #verif daca toate campurile sunt json
    if 'data' not in data or 'sens' not in data or 'idPersoana' not in data or 'idPoarta' not in data:
        return jsonify({"error": "Missing data fields"}), 400

    try:
        db = Database()

        #insereaza date in db
        db.cursor.execute('''
            INSERT INTO access (id_persoana, ora, sens, poarta)
            VALUES (?, ?, ?, ?)
        ''', (data['idPersoana'], data['data'], data['sens'], f"Poarta{data['idPoarta']}"))
        db.connection.commit()
        db.close()

        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


