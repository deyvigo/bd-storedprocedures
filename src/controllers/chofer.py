from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.database import Database



class ChoferController:
    
    @staticmethod
    @jwt_required()
    def register_chofer():
        db = Database().connection()
        try:
            data = request.json
            with db.cursor() as cursor:
                cursor.callproc('sp_register_chofer', [data['nombre'], data['apellido_pat'], data['apellido_mat'], data['dni'], data['sexo'],0,0,""])
                cursor.execute("SELECT @_sp_register_chofer_6 AS last_id, @_sp_register_chofer_7 AS rows_affected, @_sp_register_chofer_8 AS error_message;")
                result = cursor.fetchone()
                rows_affected = result['rows_affected']
                last_id = result['last_id']
                error_message = result['error_message']
                
                if error_message:
                    return jsonify({ 'error': error_message }), 400

                return jsonify({
                'message': 'Chofer registrado exitosamente',
                'rows_affected': rows_affected,
                'last_id': last_id
                }), 201
        except Exception as e:
            return jsonify({'error': f'No se pudo registrar el chofer. {e}'}), 500        
        finally:
            db.close()
    
    @staticmethod
    @jwt_required()
    def get_all_hired_choferes():
        db = Database().connection()
        try:
            with db.cursor() as cursor:
                cursor.callproc('sp_get_hired_chofer', [])
                response = cursor.fetchall()
        except Exception as e:
            return jsonify({'error': f'No se pudo obtener los choferes contratados. {e}'}), 500
        finally:
            db.close()
        if not response:
            return jsonify({ 'error': 'No tienes choferes contratados' }), 404
        return jsonify(response), 200
    
    @staticmethod
    @jwt_required()
    def get_fired_choferes():
        db = Database().connection()
        try:
            with db.cursor() as cursor:
                cursor.callproc('sp_get_fired_chofer', [])
                response = cursor.fetchall()
        except Exception as e:
            return jsonify({'error': f'No se pudo obtener los choferes contratados. {e}'}), 500
        finally:
            db.close()   

    @staticmethod
    @jwt_required()
    def get_free_choferes():
        db = Database().connection()
        try:
            data = request.json
            print("data",data)
            with db.cursor() as cursor:
                cursor.callproc('sp_get_free_chofer', [data['date']])
                response = cursor.fetchall()
        except Exception as e:
            return jsonify({'error': f'No se pudo obtener los choferes contratados. {e}'}), 500
        finally:
            db.close()
        if not response:
            return jsonify({ 'error': 'No tienes choferes contratados' }), 404
        return jsonify(response), 200
    
    @staticmethod
    @jwt_required()
    def update_status_chofer():
        db = Database().connection()
        try:
            data = request.json
            with db.cursor() as cursor:
                cursor.callproc('sp_update_status_chofer_by_id', [data['id_chofer'],0,""])
                cursor.execute("SELECT @_sp_update_status_chofer_by_id_1 AS rows_affected, @_sp_update_status_chofer_by_id_2 AS error_message;")
                result = cursor.fetchone()
                rows_affected = result['rows_affected']
                error_message = result['error_message']
                
                if error_message:
                    return jsonify({ 'error': error_message }), 400

                return jsonify({
                'message': 'Chofer estado actualizado exitosamente',
                'rows_affected': rows_affected,
                }), 201
        except Exception as e:
            return jsonify({'error': f'No se pudo actualizar estado al chofer. {e}'}), 500        
        finally:
            db.close()
        if result and result['error_message']:
            return jsonify({ 'error': result['error_message'] }), 400
        
        
    @staticmethod
    @jwt_required()
    def update_chofer():
        db = Database().connection()
        try:
            data= request.json
            with db.cursor() as cursor:
                cursor.callproc('sp_update_chofer_by_id',[data['id_chofer'],data['nombre'],data['apellido_pat'],data['apellido_mat'], data['dni'],data['sexo'],0,""])
                cursor.execute("SELECT @_sp_update_chofer_by_id_6 AS rows_affected, @_sp_update_chofer_by_id_7 AS error_message;")
                result = cursor.fetchone()
                rows_affected = result['rows_affected']
                error_message = result['error_message']
                
                if error_message:
                    return jsonify({ 'error': error_message }), 400

                return jsonify({
                'message': 'Chofer estado actualizado exitosamente',
                'rows_affected': rows_affected,
                }), 201
        except Exception as e:
            return jsonify({'error': f'No se pudo actualizar el chofer. {e}'}), 500
        finally:
            db.close()
        if result and result['error_message']:
            return jsonify({ 'error': result['error_message'] }), 400
        