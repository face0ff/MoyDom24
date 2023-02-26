define({ "api": [
  {
    "type": "post",
    "url": "/auth/login",
    "title": "Login",
    "version": "1.0.0",
    "name": "Login",
    "group": "Auth",
    "description": "<p>Логин пользователя, в header необходимо передать через basic авторизацию логин:пароль в base64</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "string",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Логин и пароль в base64.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Header-Example:",
          "content": "{\n    \"Authorization\": \"Basic KzM4MDkzMTIzNDU2NzoxMTExMTE=\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "access_token",
            "description": "<p>Токен пользователя.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"code\": 200,\n    \"status\": \"success\",\n    \"message\": \"\",\n    \"data\": {\n        \"access_token\": \"EjniWdbzJob2O5mSn_qfidDGbUEIdjJC\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\": {\n        \"name\": \"Unauthorized\",\n        \"message\": \"Your request was made with invalid credentials.\",\n        \"code\": 0,\n        \"status\": 401,\n        \"type\": \"yii\\\\web\\\\UnauthorizedHttpException\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "filename": "api/modules/v1/controllers/AuthController.php",
    "groupTitle": "Auth"
  },
  {
    "type": "get",
    "url": "/message/get?id=:id",
    "title": "Get",
    "version": "1.0.0",
    "name": "Get",
    "group": "Message",
    "description": "<p>Получить полную информацию по сообщению по id. Статус прочитанного передается в атрибуте &quot;isUserView&quot; <br/> Статусы status: <br/> 0 - неактивно <br/> 5 - ожидает очереди <br/> 10 - отправлено <br/> Типы type: <br/> default - общий <br/> invoice - квитанция <br/> house - дом <br/> pay - оплата <br/> push - пуш-уведомление</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "string",
            "optional": false,
            "field": "Authorization",
            "description": "<p>токен пользователя.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Header-Example:",
          "content": "{\n    \"Authorization\": \"Bearer kGjl32jEysdZpAtlliGuKH8OF5ESIb32\"\n}",
          "type": "json"
        }
      ]
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id квартиры.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "array",
            "optional": false,
            "field": "message",
            "description": "<p>Данные сообщения.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"code\": 200,\n    \"status\": \"success\",\n    \"message\": \"\",\n    \"data\": {\n        \"message\": {\n            \"id\": 7,\n            \"name\": \"Пришла платежка за Август\",\n            \"description\": \"Оплатите квитанцию за Август полный текст\",\n            \"type\": \"pay\",\n            \"status\": 10,\n            \"created_at\": 1504201149,\n            \"updated_at\": 1504201149,\n            \"invoice_id\": 6,\n            \"isUserView\": true\n        }\n    }\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 403 Forbidden\n{\n    \"code\": 403,\n    \"status\": \"error\",\n    \"message\": \"Access not allowed or object does not exist.\",\n    \"data\": []\n}",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\": {\n        \"name\": \"Bad Request,\n        \"message\": \"Missing required parameters: id\",\n        \"code\": 0,\n        \"status\": 400,\n        \"type\": \"yii\\\\web\\\\BadRequestHttpException\"\n    }\n}",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\": {\n        \"name\": \"Unauthorized\",\n        \"message\": \"Your request was made with invalid credentials.\",\n        \"code\": 0,\n        \"status\": 401,\n        \"type\": \"yii\\\\web\\\\UnauthorizedHttpException\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "filename": "api/modules/v1/controllers/MessageController.php",
    "groupTitle": "Message"
  },
  {
    "type": "get",
    "url": "/message/get-list?id=:id&offset=:offset&limit=:limit",
    "title": "Get List",
    "version": "1.0.0",
    "name": "Get_List",
    "group": "Message",
    "description": "<p>Получить список сообщений пользователя. Статус прочитанного передается в атрибуте &quot;isUserView&quot;. Для выгрузки порциями, использовать параметры offset + limit.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "string",
            "optional": false,
            "field": "Authorization",
            "description": "<p>токен пользователя.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Header-Example:",
          "content": "{\n    \"Authorization\": \"Bearer kGjl32jEysdZpAtlliGuKH8OF5ESIb32\"\n}",
          "type": "json"
        }
      ]
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": true,
            "field": "id",
            "description": "<p>Id сообщения, чтобы вернуть все сообщения с id &gt; указанного для данного запроса.</p>"
          },
          {
            "group": "Parameter",
            "type": "integer",
            "optional": true,
            "field": "offset",
            "description": "<p>Сколько сообщений пропустить при выборке. Для выгрузки порциями. По-умолчанию: 0.</p>"
          },
          {
            "group": "Parameter",
            "type": "integer",
            "optional": true,
            "field": "limit",
            "description": "<p>Сколько сообщений выгрузить. По-умолчанию: -1. Максимальное значение: 2000.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "array",
            "optional": false,
            "field": "messages",
            "description": "<p>Данные сообщений.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"code\": 200,\n    \"status\": \"success\",\n    \"message\": \"\",\n    \"data\": {\n        \"messages\": [\n            {\n                \"id\": 7,\n                \"name\": \"Пришла платежка за Август\",\n                \"description\": \"Оплатите квитанцию за Август полный текст\",\n                \"type\": \"pay\",\n                \"status\": 10,\n                \"created_at\": 1504201149,\n                \"updated_at\": 1504201149,\n                \"invoice_id\": 6,\n                \"isUserView\": true\n            },\n            {\n                \"id\": 8,\n                \"name\": \"Пришла платежка за Август\",\n                \"description\": \"Оплатите квитанцию за Август полный текст\",\n                \"type\": \"pay\",\n                \"status\": 10,\n                \"created_at\": 1504201149,\n                \"updated_at\": 1504201149,\n                \"invoice_id\": 8,\n                \"isUserView\": false\n            }\n        ]\n    }\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 403 Forbidden\n{\n    \"code\": 403,\n    \"status\": \"error\",\n    \"message\": \"Access not allowed or object does not exist.\",\n    \"data\": []\n}",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\": {\n        \"name\": \"Unauthorized\",\n        \"message\": \"Your request was made with invalid credentials.\",\n        \"code\": 0,\n        \"status\": 401,\n        \"type\": \"yii\\\\web\\\\UnauthorizedHttpException\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "filename": "api/modules/v1/controllers/MessageController.php",
    "groupTitle": "Message"
  },
  {
    "type": "post",
    "url": "/message/set-user-view",
    "title": "Set Message View for User",
    "version": "1.0.0",
    "name": "Set_User_View",
    "group": "Message",
    "description": "<p>Отметить сообщение как прочитанное.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "string",
            "optional": false,
            "field": "Authorization",
            "description": "<p>токен пользователя.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Header-Example:",
          "content": "{\n    \"Authorization\": \"Bearer kGjl32jEysdZpAtlliGuKH8OF5ESIb32\"\n}",
          "type": "json"
        }
      ]
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id сообщения.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"code\": 200,\n    \"status\": \"success\",\n    \"message\": \"Message read.\",\n    \"data\": []\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 403 Forbidden\n{\n    \"code\": 403,\n    \"status\": \"error\",\n    \"message\": \"Access not allowed or object does not exist.\",\n    \"data\": []\n}",
          "type": "json"
        }
      ]
    },
    "filename": "api/modules/v1/controllers/MessageController.php",
    "groupTitle": "Message"
  },
  {
    "type": "get",
    "url": "/user/get",
    "title": "Get",
    "version": "1.0.0",
    "name": "Get",
    "group": "User",
    "description": "<p>Получение информации о пользователе, по токену. <br/> Статусы status: <br/> 0 - удален <br/> 5 - новый <br/> 10 - активирован</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "string",
            "optional": false,
            "field": "Authorization",
            "description": "<p>токен пользователя.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Header-Example:",
          "content": "{\n    \"Authorization\": \"Bearer EjniWdbzJob2O5mSn_qfidDGbUEIdjJC\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "array",
            "optional": false,
            "field": "user",
            "description": "<p>Данные пользователя</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"code\": 200,\n    \"status\": \"success\",\n    \"message\": \"\",\n    \"data\": {\n        \"user\": {\n            \"id\": 1,\n            \"uid\": \"0002\",\n            \"email\": \"user2@user.com\",\n            \"status\": 10,\n            \"created_at\": 1504201149,\n            \"updated_at\": 1504201149,\n            \"profile\": {\n                \"id\": 1,\n                \"firstname\": \"Александр\",\n                \"lastname\": \"Пушкин\",\n                \"middlename\": \"Сергеевич\",\n                \"birthdate\": \"1990-06-23\",\n                \"phone\": \"+380932222222\",\n                \"viber\": \"vib123456\",\n                \"telegram\": \"teleg123456\",\n                \"image\": \"/upload/User/2/avatar.png\",\n                \"user_id\": 1\n            }\n        }\n    }\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\": {\n        \"name\": \"Unauthorized\",\n        \"message\": \"Your request was made with invalid credentials.\",\n        \"code\": 0,\n        \"status\": 401,\n        \"type\": \"yii\\\\web\\\\UnauthorizedHttpException\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "filename": "api/modules/v1/controllers/UserController.php",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/get-flats",
    "title": "Get Flats",
    "version": "1.0.0",
    "name": "Get_Flats",
    "group": "User",
    "description": "<p>Получить список квартир пользователя, по токену.</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "string",
            "optional": false,
            "field": "Authorization",
            "description": "<p>токен пользователя.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Header-Example:",
          "content": "{\n    \"Authorization\": \"Bearer kGjl32jEysdZpAtlliGuKH8OF5ESIb32\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "array",
            "optional": false,
            "field": "flats",
            "description": "<p>Список квартир.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"code\": 200,\n    \"status\": \"success\",\n    \"message\": \"\",\n    \"data\": {\n        \"flats\": [\n            {\n                \"id\": 2,\n                \"flat\": \"2\",\n                \"created_at\": 1504201149,\n                \"updated_at\": 1504201149,\n                \"house_id\": 1,\n                \"user_id\": 3,\n                \"section_id\": 1,\n                \"riser_id\": 1,\n                \"floor_id\": 1,\n                \"debt\": 3900,\n                \"balance\": 2450,\n                \"house\": {\n                    \"id\": 1,\n                    \"name\": \"Жемчужина 1\",\n                    \"address\": \"ул. Пушкина, 4\",\n                    \"image1\": \"/upload/House/1/image1.jpg\",\n                    \"image2\": \"/upload/House/1/image2.jpg\",\n                    \"image3\": \"/upload/House/1/image3.jpg\",\n                    \"image4\": \"/upload/House/1/image4.jpg\",\n                    \"image5\": \"/upload/House/1/image5.jpg\",\n                    \"created_at\": 1504201149,\n                    \"updated_at\": 1504201149\n                },\n                \"section\": {\n                    \"id\": 1,\n                    \"name\": \"Секция 1\"\n                },\n                \"riser\": {\n                    \"id\": 1,\n                    \"name\": \"Cтояк 1\"\n                },\n                \"floor\": {\n                    \"id\": 1,\n                    \"name\": \"Этаж 1\"\n                }\n            },\n            {\n                \"id\": 10,\n                \"flat\": \"104\",\n                \"created_at\": 1504201149,\n                \"updated_at\": 1504201149,\n                \"balance\": 0,\n                \"debt\": 0,\n                \"house\": {\n                    \"id\": 2,\n                    \"name\": \"Жемчужина 2\",\n                    \"address\": \"ул. Зеленая, 12\",\n                    \"image1\": \"/upload/House/2/image1.jpg\",\n                    \"image2\": \"/upload/House/2/image2.jpg\",\n                    \"image3\": \"/upload/House/2/image3.jpg\",\n                    \"image4\": \"/upload/House/2/image4.jpg\",\n                    \"image5\": \"/upload/House/2/image5.jpg\",\n                    \"created_at\": 1504201149,\n                    \"updated_at\": 1504201149\n                },\n                \"section\": {\n                    \"id\": 4,\n                    \"name\": \"Секция 1\"\n                },\n                \"riser\": {\n                    \"id\": 4,\n                    \"name\": \"Cтояк 1\"\n                },\n                \"floor\": {\n                    \"id\": 16,\n                    \"name\": \"Этаж 6\"\n                }\n            }\n        ]\n    }\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\": {\n        \"name\": \"Unauthorized\",\n        \"message\": \"Your request was made with invalid credentials.\",\n        \"code\": 0,\n        \"status\": 401,\n        \"type\": \"yii\\\\web\\\\UnauthorizedHttpException\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "filename": "api/modules/v1/controllers/UserController.php",
    "groupTitle": "User"
  }
] });
