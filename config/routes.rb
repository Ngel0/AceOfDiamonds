Rails.application.routes.draw do
  get 'home/index'
  root 'home#index'
  get '/letter', to: 'letter#index'
  get '/letter/new', to: 'letter#new'
  post '/letter', to: 'letter#create'

  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
