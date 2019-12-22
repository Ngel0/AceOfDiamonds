class HomeController < ApplicationController
  def index
  end

  def letter
    inpath = 'lib/text.txt'
    outpath = 'lib/textout.txt'
    session[:intext] = params[:intext]
    File.open(inpath, 'w'){ |file| file.write session[:intext] }
    `py lib/script.py #{inpath} #{outpath}`
    value = File.open(outpath, 'r'){ |file| file.read }
    session[:outtext] = value
    redirect_to "/"
  end
end