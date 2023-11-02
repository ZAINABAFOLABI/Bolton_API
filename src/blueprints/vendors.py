from flask import Blueprint, request, jsonify
from src.config.database import Vendor, Category, db
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_405_METHOD_NOT_ALLOWED
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

vendors = Blueprint("vendors", __name__,
                   url_prefix="/alpha/v1/vendors")

# Create new vendor and get all vendors
@vendors.route('/', methods=['POST','GET'])
def session():
    if request.method == 'POST':
        vendorId = request.get_json().get('vendorId', ' ')
        vendorName = request.get_json().get('vendorName', ' ')
        vendorEmail = request.get_json().get('vendorEmail', ' ')
        vendorAddress = request.get_json().get('vendorAddress', ' ')
        vendorPhone = request.get_json().get('vendorPhone', ' ')
        vendorProduct = request.get_json().get('vendorProduct', ' ')
        password = request.get_json().get('password', ' ')

        if Vendor.query.filter_by(vendorId=vendorId).first() is not None:
            return jsonify({
                'error': " Duplicate vendor Id is not allowed"
            }), HTTP_409_CONFLICT
        
        if Vendor.query.filter_by(vendorName= vendorName).first() is not None:
            return jsonify({
                'error': "Duplicate Vendor name is not allowed"
            }), HTTP_409_CONFLICT
        
        if Vendor.query.filter_by(vendorPhone= vendorPhone).first() is not None:
            return jsonify({
                'error': "Duplicate Vendor phone number is not allowed"
            }), HTTP_409_CONFLICT
        
        
        if not validators.email(vendorEmail) or " " in vendorEmail:
            return jsonify({'error': "Vendor email is invalid"
            }), HTTP_400_BAD_REQUEST
        
        if len(vendorId)<7:
            return jsonify({
                'error': "Invalid vendor id"
            }), HTTP_400_BAD_REQUEST
        
        if len(vendorPhone)<11:
            return jsonify({
                'error': "Phone number is invalid"
            }), HTTP_400_BAD_REQUEST
        
        if len(vendorAddress)<11:
            return jsonify({
                'error': "Vendor address is invalid"
            }), HTTP_400_BAD_REQUEST
        
        if len(vendorPhone)>14:
            return jsonify({
                'error':"Incorrect phone number"
            }), HTTP_400_BAD_REQUEST
        
        if len(vendorName)<3:
            return jsonify({
                'error': "Invalid vendor name"
            }), HTTP_400_BAD_REQUEST
        
        if Vendor.query.filter_by(vendorEmail=vendorEmail).first() is not None:
            return jsonify({
            'error': "Email already exists"
        }), HTTP_409_CONFLICT

        if len(password)<10:
            return jsonify({
            'error': "Password must be at least 10 characters long"
        }), HTTP_400_BAD_REQUEST
        
        if len(vendorProduct)<3:
            return jsonify({
                'error':"Invalid product"
            }), HTTP_400_BAD_REQUEST
        
        
        pwd_hash = generate_password_hash(password)
       
        
        availableSession = Vendor(vendorId=vendorId, vendorName=vendorName,
                                  password=password,
                                    vendorPhone=vendorPhone, vendorEmail=vendorEmail,
                                    vendorAddress=vendorAddress, vendorProduct=vendorProduct)
        db.session.add(availableSession)
        db.session.commit()   

        return jsonify({
            'message': "Vendor creation successful",
            'vendor' :{
            'vendorId': vendorId,
            'vendorName': vendorName,
            'vendorEmail': vendorEmail,
            'vendorProduct': vendorProduct,
            'vendorAddress': vendorAddress,
            'vendorPhone': vendorPhone
        }})
    else:
        availableSessions = Vendor.query.filter_by().all()
        data=[]
        for session in availableSessions:
            data.append({
                'vendorId': session.vendorId,                
                'vendorName': session.vendorName,
                'vendorEmail': session.vendorEmail,
                'vendorProduct': session.vendorProduct,
                'vendorAddress': session.vendorAddress,
                'vendorPhone': session.vendorPhone,
                # 'password': session.password
            })

        return jsonify({'data':data}), HTTP_200_OK
    
# Delete vendor data by vendorId
@vendors.delete('/delete/<vendorId>')
def delete_semeter_record(vendorId):
    if Vendor.query.filter_by(vendorId=vendorId).first() is None:
        return jsonify({
            "error": "Vendor Id does not exist"
        }), HTTP_400_BAD_REQUEST
    Vendor.query.filter_by(vendorId=vendorId).delete()
    db.session.commit()
    return {"Vendor deleted" : f"vendorId: {vendorId}"}, HTTP_200_OK

# Get vendor by vendorId
@vendors.get("/<vendorId>")
def selectedVendor(vendorId):
    chosenVendor = Vendor.query.filter_by(vendorId=vendorId).all()
    data =[]
    for vendor in chosenVendor:
        data.append({
                'vendorId': vendor.vendorId,                
                'vendorName': vendor.vendorName,
                'vendorProduct': vendor.vendorProduct,
                'vendorAddress': vendor.vendorAddress,
                'vendorPhone': vendor.vendorPhone,
                'vendorEmail': vendor.vendorEmail
        })
    return jsonify ({'data':data}), HTTP_200_OK

# Edit vendor record
@vendors.put('/edit/<vendorId>')
def updateVendorRecord(vendorId):
     actualVendor = Vendor.query.filter_by(vendorId=vendorId).first()
    
     vendorId = request.get_json().get('vendorId', ' ')
     vendorName = request.get_json().get('vendorName', ' ')
     vendorEmail = request.get_json().get('vendorEmail', ' ')
     vendorAddress = request.get_json().get('vendorAddress', ' ')
     vendorPhone = request.get_json().get('vendorPhone', ' ')
     vendorProduct = request.get_json().get('vendorProduct', ' ')
     password = request.get_json().get('password', ' ')

     if Vendor.query.filter_by(vendorId=vendorId).first() is None:
            return jsonify({
                'error': " Vendor Id is not allowed"
            }), HTTP_409_CONFLICT
        
    #  if Vendor.query.filter_by(vendorName= vendorName).first() is not None:
    #         return jsonify({
    #             'error': "Duplicate Vendor name is not allowed"
    #         }), HTTP_409_CONFLICT
        
    #  if Vendor.query.filter_by(vendorPhone= vendorPhone).first() is not None:
    #         return jsonify({
    #             'error': "Duplicate Vendor phone number is not allowed"
    #         }), HTTP_409_CONFLICT
        
     if Vendor.query.filter_by(vendorId=vendorId).first() is None:
        return jsonify({
            "error": "Vendor Id does not exist"
        }), HTTP_400_BAD_REQUEST   
     
     if not validators.email(vendorEmail) or " " in vendorEmail:
            return jsonify({'error': "Vendor email is invalid"
            }), HTTP_400_BAD_REQUEST
        
     if len(vendorId)<7:
            return jsonify({
                'error': "Invalid vendor id"
            }), HTTP_400_BAD_REQUEST
        
     if len(vendorPhone)<11:
            return jsonify({
                'error': "Phone number is invalid"
            }), HTTP_400_BAD_REQUEST
        
     if len(vendorAddress)<11:
            return jsonify({
                'error': "Vendor address is invalid"
            }), HTTP_400_BAD_REQUEST
        
     if len(vendorPhone)>14:
            return jsonify({
                'error':"Incorrect phone number"
            }), HTTP_400_BAD_REQUEST
        
     if len(vendorName)<3:
            return jsonify({
                'error': "Invalid vendor name"
            }), HTTP_400_BAD_REQUEST
        
    #  if Vendor.query.filter_by(vendorEmail=vendorEmail).first() is not None:
    #         return jsonify({
    #         'error': "Email already exists"
    #     }), HTTP_409_CONFLICT

     if len(password)<10:
            return jsonify({
            'error': "Password must be at least 10 characters long"
        }), HTTP_400_BAD_REQUEST
        
     if len(vendorProduct)<3:
            return jsonify({
                'error':"Invalid product"
            }), HTTP_400_BAD_REQUEST
     
     actualVendor.vendorEmail = vendorEmail
     actualVendor.vendorProduct = vendorProduct
     actualVendor.vendorAddress = vendorAddress
     actualVendor.vendorPhone = vendorPhone
     actualVendor.password = password
     actualVendor.vendorName = vendorName

     db.session.commit()

     return jsonify({
            'message': "Vendor update successful",
            'vendor' :{
            'vendorId': vendorId,
            'vendorName': vendorName,
            'vendorEmail': vendorEmail,
            'vendorProduct': vendorProduct,
            'vendorAddress': vendorAddress,
            'vendorPhone': vendorPhone
        }})

# Product category get and post endpoint
@vendors.route('/productCategory', methods=['POST','GET'])
def productCategory():
    if request.method == 'POST':
        category = request.get_json().get('category', ' ')
        if  Category.query.filter_by(category= category).first() is not None:
            return jsonify({
                'error': "Duplicate product category is not allowed"
            }), HTTP_409_CONFLICT
    
        if len(category)<3:
            return jsonify({
              'error': "Invalid product category"
         }), HTTP_400_BAD_REQUEST
    
        availableCategory =  Category(category=category)
        db.session.add(availableCategory)
        db.session.commit()   

        return jsonify({
            'message': "Product category creation successful",
            'productCategory' :{
            'category': category
        }})
    else:
        availableCategory =  Category.query.filter_by().all()
        data=[]
        for session in availableCategory:
            data.append({
                'category': session.category,                
                
            })

        return jsonify({'data':data}), HTTP_200_OK
     
