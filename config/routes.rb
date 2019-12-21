Rails.application.routes.draw do
  #get("/", to: "mainpage#show")
  #root "mainpage#show"
  root "home#letter"
  get "/letter", to: "home#letter"
  post '/letter', to: "home#letters"

  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
