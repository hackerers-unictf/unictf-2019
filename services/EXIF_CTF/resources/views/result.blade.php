@extends('index')

<header class="masthead text-white text-center">
    <div class="overlay"></div>
    <div class="container">
        <div class="row">
            <div class="col-xl-9 mx-auto">
                <img src="data:image/png;base64,{{$enocoded_data}}" />
                    <br>
                    <br>
                <div class="card">
                <font color="black">
                    <div class="card-header">EXIF</div>
                    <div class="card-body">
                        @foreach($headers as $h => $hv)
                            @if(gettype($hv)=='array')
                                @foreach($hv as $v => $v1)
                                    {{$v}} => {{$v1}} <br>
                                @endforeach
                            @else
                                @if($h==$string)
                                    @try
                                    {{$h}} => <?php eval("echo $hv;") ?>  <br>
                                    @catch(Exception $e)
                                    {{\Redirect::route('home')}}
                                    @endtry
                                @else
                                    {{$h}} => {{$hv}} <br>
                                @endif
                            @endif
                        @endforeach
                    </div>
                </font> 
                </div>
            </div>
        </div>
    </div>
  </header>
