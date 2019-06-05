<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Redirect;
class HomeController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function index()
    {
        return view('index');
    }
    
    public function show(Request $request){
        try{
            if($request['file']){
                $count=0;
                $before="";
                $file=$request['file'];
                $fp = fopen($file, 'rb');
                $mime=mime_content_type($fp);
                if($mime=="image/jpeg"){
                    $headers=exif_read_data($fp);
                    foreach($headers as $h => $value){
                        if($count==3)
                            return Redirect::route('home');
                        if($value==$before){
                            $count++;
                            $before=$value;
                        }
                    }

                    $image= file_get_contents($file);
                    $n=rand(0,4);
                    $string=config('s')[$n];
                    $enocoded_data= base64_encode($image);
                    return view('result')->with(compact('enocoded_data','headers','string'));
                }
                else{
                    return Redirect::route('home');
                }
            }
            else{
                return Redirect::route('home');
            }
        }
        catch (\Exception $e) {
            return Redirect::route('home');
        }
    }

}
