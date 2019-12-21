class HomeController < ApplicationController
  def index

  end

  def letter

  end

  def letters
    #value = `py E:/Desktop/PycharmProjects/Project2/wRuby.py человек_NOUN`

    # записать в файл before
    #params[:inptext]
    inputstr = params[:inptext]#'Скажи дядя ведь не даром' #считывается с сайта
    File.open('E:/Desktop/PycharmProjects/Project2/books_before/text.txt', 'w'){ |file| file.write inputstr }
    #File.open('C:/text.txt', 'w'){ |file| file.write inputstr }
    #File.close ??
    `py copy2.py`
    value = File.open('E:/Desktop/PycharmProjects/Project2/books_after/3.0_text.txt', 'r'){ |file| file.read }
    #value = File.open('C:/3.0_text.txt', 'r'){ |file| file.read }
    session[:varin]=inputstr
    session[:varout] = value
    #session[:varout] = value
    redirect_to "/letter"
  end
end