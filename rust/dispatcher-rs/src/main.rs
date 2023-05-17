use warp::Filter;
use serde::{Deserialize, Serialize};
use rdkafka::producer::{FutureProducer, FutureRecord};
use rdkafka::util::Timeout;
use rdkafka::ClientConfig;

#[derive(Deserialize, Serialize)]
struct LineItem {
    potion: String,
    quantity: u32,
}

#[derive(Deserialize, Serialize)]
struct Order {
    line_items: Vec<LineItem>,
    order_id: String,
}

#[tokio::main]
async fn main() {
    let order_route = warp::path("order")
        .and(warp::post())
        .and(warp::body::json())
        .and_then(create_order);

    // This does not work, but I don't know how to fix it...
    let routes = order_route
        .with(warp::cors()
            .allow_any_origin()
            .allow_any_origin()
            .allow_headers(vec!["Access-Control-Request-Headers", "Content-Type"])
            .allow_methods(vec!["POST", "GET"]));

    warp::serve(routes)
        .run(([127, 0, 0, 1], 3001))
        .await;
}

async fn create_order(order: Order) -> Result<impl warp::Reply, warp::Rejection> {
    let producer: FutureProducer = ClientConfig::new()
        .set("bootstrap.servers", "localhost:9092")
        .create()
        .expect("Producer creation error");

    let order_json = serde_json::to_string(&order).expect("Could not serialize order");
    let record = FutureRecord::to("orders")
        .payload(&order_json).key(&order.order_id);

    match producer.send(record, Timeout::Never).await {
        Ok(_) => println!("Order sent successfully"),
        Err(e) => println!("Error producing order: {:?}", e),
    };

    Ok(warp::reply::with_status("Order sent to Kafka", warp::http::StatusCode::OK))
}
