Rails.application.routes.draw do
  #get("/", to: "mainpage#show")
  #root "mainpage#show"
  root "home#index"
  #get "/letter", to: "home#letter"
  post '/letter', to: "home#letter"

  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
