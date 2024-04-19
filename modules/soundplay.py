import sounddevice as sd
import soundfile as sf
 
def soundplay(url): 
	array, smp_rt = sf.read(url, dtype = 'float32')  

	sd.play(array, smp_rt)
	
	status = sd.wait()  
	
	sd.stop()