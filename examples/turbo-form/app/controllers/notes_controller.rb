class NotesController < ApplicationController
  def new
    @note = Note.new
  end

  def create
    @note = Note.new(params.expect(note: %i[title body]))
    if @note.save
      redirect_to @note, status: :see_other
    else
      render :new, status: :unprocessable_content
    end
  end

  def show
    @note = Note.find(params[:id])
  end
end
