# **Weather App - Backend with GraphQL and MongoDB**

A Python server using Flask, GraphQL, and MongoDB to fetch, store, and serve weather data through external APIs and GraphQL.

---

## **Main Features**

1. **REST Endpoint (`/fetch-weather`)**  
   - Fetches weather data from the Stormglass API.  
   - Stores the data in the MongoDB database.  
   - Limits external API calls to **10 per day**.  

2. **GraphQL Endpoint (`/graphql`)**  
   - Provides access to weather data stored in MongoDB.  
   - Does not make external API calls.  

3. **MongoDB Integration**  
   - All data is stored in a MongoDB database.  
   - Accessible for direct verification or updates.  

---

## **Requirements**

Make sure the following tools are installed in your environment:  

- **Docker**  
- **Docker Compose**  

---

## **Setup Instructions**

To launch the application, use Docker Compose:

```bash
docker-compose up --build
```

---

## **Usage**

### **REST Endpoint (`/fetch-weather`)**

Make a `GET` request to fetch weather data and save it to MongoDB:

```bash
curl http://localhost:5000/fetch-weather
```

**Sample Response:**

```json
{
  "status": "success",
  "message": "Data saved successfully"
}
```

---

### **Verifying Data in MongoDB**

To verify that the data has been saved in MongoDB, follow these steps:

1. Access the MongoDB container:

   ```bash
   docker exec -it mongo bash
   ```

2. Open the MongoDB shell:

   ```bash
   mongosh
   ```

3. Select the database:

   ```bash
   use weather_db
   ```

4. View the documents in the collection:

   ```bash
   db.weather_data.find().pretty()
   ```

---

