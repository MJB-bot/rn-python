from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        messages = error.messages
        if isinstance(messages, dict):
            flat = []
            for field, msgs in messages.items():
                if isinstance(msgs, list):
                    flat.extend(msgs)
                else:
                    flat.append(str(msgs))
            msg = '; '.join(str(m) for m in flat)
        else:
            msg = str(messages)
        logger.warning(f'ValidationError: {msg}')
        return jsonify({'success': False, 'message': msg}), 400

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({'success': False, 'message': str(error.description or '请求参数错误')}), 400

    @app.errorhandler(401)
    def handle_unauthorized(error):
        return jsonify({'success': False, 'message': str(error.description or '未授权')}), 401

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'success': False, 'message': str(error.description or '资源不存在')}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({'success': False, 'message': '请求方法不允许'}), 405

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db_msg = str(error.orig) if error.orig else str(error)
        logger.error(f'IntegrityError: {db_msg}')
        if 'Duplicate entry' in db_msg:
            return jsonify({'success': False, 'message': '数据已存在，请检查唯一字段'}), 400
        return jsonify({'success': False, 'message': '数据库完整性错误'}), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        orig = getattr(error, 'orig', None)
        detail = str(orig) if orig else str(error)
        logger.exception(f'SQLAlchemyError: {detail}')
        if 'connect' in detail.lower() or 'timeout' in detail.lower():
            return jsonify({'success': False, 'message': '数据库连接异常，请稍后重试'}), 500
        return jsonify({'success': False, 'message': f'数据库操作异常: {detail}'}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.exception(f'Unexpected error: {str(error)}')
        return jsonify({'success': False, 'message': f'服务器内部错误: {str(error)}'}), 500
