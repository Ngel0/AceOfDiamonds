class LetterController < ApplicationController
  def index
  end

  def new
  end

  def create
    modelpath = 'lib/neural.model'
    `py lib/download.py #{modelpath}` unless File.file? modelpath
    inpath = 'lib/text.txt'
    outpath = 'lib/textout.txt'
    session[:intext] = params[:intext]
    File.open(inpath, 'w'){ |file| file.write session[:intext] }
    `py lib/script.py #{inpath} #{outpath} #{modelpath}`
    value = File.open(outpath, 'r'){ |file| file.read }
    session[:outtext] = value
    redirect_to '/letter/new'
  end
end
