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
                cursor.callproc('sp_register_chofer', [data['nombre'], data['apellido_pat'], data['apellido_mat'], data['dni'], data['sexo'] ])
                result = cursor.fetchone()
        except Exception as e:
            return jsonify({'error': f'No se pudo registrar el chofer. {e}'}), 500        
        finally:
            db.close()
        if result and result['error_message']:
            return jsonify({ 'error': result['error_message'] }), 400
    
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
            with db.cursor() as cursor:
                cursor.callproc('sp_get_free_chofer', [])
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
                cursor.callproc('sp_update_status_chofer', [data['id_chofer']])
                result = cursor.fetchone()
        except Exception as e:
            return jsonify({'error': f'No se pudo registrar el chofer. {e}'}), 500        
        finally:
            db.close()
        if result and result['error_message']:
            return jsonify({ 'error': result['error_message'] }), 400
        
        
    @staticmethod
    @jwt_required
    def update_chofer():
        db = Database().connection()
        try:
            data= request.json
            with db.cursor() as cursor:
                cursor.callproc('sp_update_chofer_by_id',[data['id_chofer'],data['nombre'],data['apellido_pat'],data['apellido_mat'], data['dni'],data['sexo']])
                result = cursor.fetchone()
        except Exception as e:
            return jsonify({'error': f'No se pudo actualizar el chofer. {e}'}), 500
        finally:
            db.close()
        if result and result['error_message']:
            return jsonify({ 'error': result['error_message'] }), 400
        