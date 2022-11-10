cd Gatewayservice
docker build --tag gatewayservice .

cd ../LoyaltyService
docker build --tag loyaltyservice .

cd ../ReservationService
docker build --tag reservationservice .

cd ../PaymentService
docker build --tag paymentservice .