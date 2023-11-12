from flask import Blueprint, request, jsonify
from src.config.database import db, Contact
import validators
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_405_METHOD_NOT_ALLOWED

contact = Blueprint("contact", __name__,
                   url_prefix="/zainab/v1/contact")

# Get contact message and post message

@contact.route('/', methods= ['GET', 'POST'])
def session():
    if request.method == 'POST':
        name = request.get_json().get('name', ' ')
        email = request.get_json().get('email', ' ')
        phone = request.get_json().get('phone', ' ')
        message = request.get_json().get('message', ' ')

        if not validators.email(email) or " " in email:
            return jsonify({'error': "Email is invalid"
            }), HTTP_400_BAD_REQUEST
        
        if len(name)<3:
            return jsonify({'error': "Name is too short"

            }), HTTP_400_BAD_REQUEST
        
        if len(phone)<11:
            return jsonify ({'error': "Phone number is incorrect"

            }), HTTP_400_BAD_REQUEST
        
        if len(phone)>13:
            return jsonify ({'error': "Phone number is incorrect"

            }), HTTP_400_BAD_REQUEST
        
        if len(message)<10:
             return jsonify ({'error': "Message is too short"

            }), HTTP_400_BAD_REQUEST
        
          
        availableSession = Contact(name=name, phone=phone,
                                  email=email,
                                    message=message)
        db.session.add(availableSession)
        db.session.commit()   

        return jsonify({
            'message': "Message sent",
            'vendor' :{
            'name': name,
            'phone': phone,
            'email': email,
            'message': message
        }})
    else:
        availableSessions = Contact.query.filter_by().all()
        data=[]
        for session in availableSessions:
            data.append({
                'name': session.name,                
                'email': session.email,
                'message': session.message,
                'phone': session.phone,
           
            })

        return jsonify({'data':data}), HTTP_200_OK
    

        
               