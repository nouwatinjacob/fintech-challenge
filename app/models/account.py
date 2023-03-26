from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class AccountModel(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_name = Column(String(50), nullable=False)
    balance = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    user = relationship('UserModel', back_populates='accounts')
    transactions = relationship('TransactionModel', back_populates='account')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'account_name': self.account_name,
            'balance': self.balance,
            'created_at': str(self.created_at),
            'user_id': self.user_id,
            'transaction_count': len(self.transactions)
        }


class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, transaction_id):
        return cls.query.filter_by(id=transaction_id).first()

    @classmethod
    def find_all_by_account_id(cls, account_id):
        return cls.query.filter_by(account_id=account_id).all()

    @classmethod
    def search_by_description(cls, account_id, description, page, per_page):
        query = cls.query.filter_by(account_id=account_id)
        if description:
            query = query.filter(cls.description.ilike(f'%{description}%'))
        return query.paginate(page=page, per_page=per_page, error_out=False)